# -*- coding: utf-8 -*-
import pandas as pd
import yfinance as yf
import json
import argparse
import sys
import os
from datetime import datetime
from config import *
from data_fetcher import get_all_stock_data, get_earnings_growth, get_fcf_yield
from valuation_scorer import calculate_valuation_score
from technical_scorer import calculate_technical_score
from extension_analyzer import classify_price_extension

# Set stdout encoding to UTF-8 for emoji support on Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Hidden Gems Stock Screener - Find undervalued quality stocks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py --market US          Scan US stocks only
    python main.py --market INDIA       Scan Indian stocks only
    python main.py --market BOTH        Scan both markets
    python main.py -m US --output custom   Custom output filename
        """
    )
    
    parser.add_argument(
        '-m', '--market',
        type=str,
        choices=['US', 'INDIA', 'BOTH', 'us', 'india', 'both'],
        default='US',
        help='Market to scan: US, INDIA, or BOTH (default: US)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Custom output filename (without extension)'
    )
    
    parser.add_argument(
        '--no-json',
        action='store_true',
        help='Skip JSON export (only create CSV)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output with more details'
    )
    
    return parser.parse_args()

def apply_market_config(market: str):
    """
    Apply market-specific configuration
    Args:
        market: 'US', 'INDIA', or 'BOTH' (case-insensitive)
    """
    global STOCK_UNIVERSE, MARKET_CAP_MIN, MARKET_CAP_MAX, MIN_AVG_VOLUME, MARKET_INDEX, OUTPUT_FILE, MARKET
    
    # Normalize to uppercase
    market = market.upper()
    MARKET = market
    
    if market == "US":
        STOCK_UNIVERSE = US_STOCK_UNIVERSE
        MARKET_CAP_MIN = US_MARKET_CAP_MIN
        MARKET_CAP_MAX = US_MARKET_CAP_MAX
        MIN_AVG_VOLUME = US_MIN_AVG_VOLUME
        MARKET_INDEX = "SPY"
        OUTPUT_FILE = "../output/stock_picks.csv"
    
    elif market == "INDIA":
        STOCK_UNIVERSE = INDIA_STOCK_UNIVERSE
        MARKET_CAP_MIN = INDIA_MARKET_CAP_MIN
        MARKET_CAP_MAX = INDIA_MARKET_CAP_MAX
        MIN_AVG_VOLUME = INDIA_MIN_AVG_VOLUME
        MARKET_INDEX = "^NSEI"
        OUTPUT_FILE = "../output/stock_picks_india.csv"
    
    elif market == "BOTH":
        STOCK_UNIVERSE = US_STOCK_UNIVERSE + INDIA_STOCK_UNIVERSE
        MARKET_CAP_MIN = min(US_MARKET_CAP_MIN, INDIA_MARKET_CAP_MIN)
        MARKET_CAP_MAX = max(US_MARKET_CAP_MAX, INDIA_MARKET_CAP_MAX)
        MIN_AVG_VOLUME = min(US_MIN_AVG_VOLUME, INDIA_MIN_AVG_VOLUME)
        MARKET_INDEX = "SPY"
        OUTPUT_FILE = "../output/stock_picks_combined.csv"
    
    return {
        'universe': STOCK_UNIVERSE,
        'market_cap_min': MARKET_CAP_MIN,
        'market_cap_max': MARKET_CAP_MAX,
        'min_volume': MIN_AVG_VOLUME,
        'index': MARKET_INDEX,
        'output_file': OUTPUT_FILE
    }

def check_market_filter():
    """Check if market index is above 200 MA"""
    index = yf.Ticker(MARKET_INDEX)
    index_hist = index.history(period='1y')
    
    if len(index_hist) < 200:
        return False, index_hist
    
    sma_200 = index_hist['Close'].rolling(window=200).mean().iloc[-1]
    current_price = index_hist['Close'].iloc[-1]
    
    return current_price > sma_200, index_hist

def apply_filters(all_data):
    """Apply hidden gems filters"""
    # Market Cap Filter
    if not (MARKET_CAP_MIN <= all_data['market_cap'] <= MARKET_CAP_MAX):
        return False, f"Market cap ${all_data['market_cap']/1e9:.1f}B (need $0.3B-$10B)"
    
    # Volume Filter
    if all_data['avg_volume'] < MIN_AVG_VOLUME:
        return False, f"Volume {all_data['avg_volume']:,.0f} (need >{MIN_AVG_VOLUME/1000:.0f}K)"
    
    return True, "Passed"

def get_action(val_score, tech_score, market_bullish):
    """
    Determine action based on scores with conservative thresholds
    Args:
        val_score: Valuation score (0-100)
        tech_score: Technical score (0-100)
        market_bullish: Whether market is bullish
    Returns:
        Tuple of (action, emoji, needs_analysis, reasoning)
    """
    thresholds = ACTION_THRESHOLDS
    
    # Apply market regime adjustment if bearish
    adjustment = 0
    if not market_bullish and not MARKET_REGIME['block_buys_in_bear']:
        adjustment = MARKET_REGIME['bearish_adjustment']
    
    # STRONG BUY - Ultra high conviction
    if (val_score >= thresholds['STRONG_BUY']['valuation_min'] + adjustment and
        tech_score >= thresholds['STRONG_BUY']['technical_min']):
        reasoning = f"Exceptional fundamentals (V:{val_score}) + Excellent timing (T:{tech_score})"
        return "STRONG_BUY", "🔥🔥", True, reasoning
    
    # BUY - High conviction
    if (val_score >= thresholds['BUY']['valuation_min'] + adjustment and
        tech_score >= thresholds['BUY']['technical_min']):
        reasoning = f"Strong fundamentals (V:{val_score}) + Good timing (T:{tech_score})"
        return "BUY", "🔥", True, reasoning
    
    # WATCH - Good fundamentals, waiting for technical setup
    if (val_score >= thresholds['WATCH']['valuation_min'] and
        thresholds['WATCH']['technical_min'] <= tech_score <= thresholds['WATCH']['technical_max']):
        reasoning = f"Strong fundamentals (V:{val_score}), but timing not optimal (T:{tech_score}). Wait for T>60"
        return "WATCH", "⏳", False, reasoning
    
    # WAIT - Great company, wrong time
    if (val_score >= thresholds['WAIT']['valuation_min'] and
        tech_score < thresholds['WAIT']['technical_max']):
        reasoning = f"Great company (V:{val_score}), but poor timing (T:{tech_score}). "
        # Add specific guidance based on technical issues
        if tech_score < 30:
            reasoning += "Wait for trend reversal and volume increase"
        elif tech_score < 40:
            reasoning += "Wait for RSI to improve and MACD to turn bullish"
        return "WAIT", "🕐", False, reasoning
    
    # SPECULATIVE - Momentum play with decent fundamentals
    if (thresholds['SPECULATIVE']['valuation_min'] <= val_score < thresholds['SPECULATIVE']['valuation_max'] and
        tech_score >= thresholds['SPECULATIVE']['technical_min']):
        reasoning = f"Decent fundamentals (V:{val_score}) + Strong momentum (T:{tech_score}). Higher risk play"
        return "SPECULATIVE", "⚠️", False, reasoning
    
    # AVOID - Market bearish and blocking buys
    if not market_bullish and MARKET_REGIME['block_buys_in_bear']:
        reasoning = f"Market bearish - holding cash. Scores: V:{val_score}, T:{tech_score}"
        return "CASH", "💰", False, reasoning
    
    # AVOID - Does not meet criteria
    reasoning = f"Below thresholds: V:{val_score} (need ≥70), T:{tech_score} (need ≥40)"
    return "AVOID", "❌", False, reasoning

def main():
    """Main execution function"""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Apply market configuration
    config = apply_market_config(args.market)
    
    # Update output file if custom name provided
    global OUTPUT_FILE
    if args.output:
        OUTPUT_FILE = f"../output/{args.output}.csv"
    
    print("=" * 60)
    print("HIDDEN GEMS STOCK SCREENER - CONSERVATIVE EDITION")
    print("=" * 60)
    print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Market: {args.market.upper()}")
    print(f"Index Filter: {config['index']}")
    print(f"Data Source: Yahoo Finance (No API limits!)")
    
    if args.verbose:
        print(f"Market Cap Range: ${config['market_cap_min']/1e9:.1f}B - ${config['market_cap_max']/1e9:.1f}B")
        print(f"Min Volume: {config['min_volume']:,}")
        print(f"Stock Universe: {len(config['universe'])} stocks")
    print()
    
    # Check market filter
    print(f"Checking market conditions ({MARKET_INDEX} 200 MA)...")
    market_bullish, spy_hist = check_market_filter()
    print(f"Market Status: {'🟢 BULLISH' if market_bullish else '🔴 BEARISH'}")
    print()
    
    results = []
    
    print(f"Scanning {len(STOCK_UNIVERSE)} stocks...")
    print("-" * 60)
    
    for i, ticker in enumerate(STOCK_UNIVERSE, 1):
        print(f"[{i}/{len(STOCK_UNIVERSE)}] {ticker}...", end=" ")
        
        try:
            # OPTIMIZED: Fetch ALL data in ONE call
            all_data = get_all_stock_data(ticker)
            
            if not all_data:
                print("❌ No data")
                continue
            
            # Apply filters
            passed, reason = apply_filters(all_data)
            if not passed:
                print(f"❌ {reason}")
                continue
            
            # Extract pre-fetched data (no additional API calls!)
            fundamentals = all_data['fundamentals']
            info = all_data['info']
            
            if not fundamentals:
                print("❌ No fundamentals")
                continue
            
            # Get earnings growth (using pre-fetched info)
            eps_yoy, eps_3y = get_earnings_growth(ticker, info)
            
            # Get FCF yield (using pre-fetched info)
            fcf_yield = get_fcf_yield(ticker, all_data['market_cap'], info)
            
            # Calculate scores
            val_score, val_details = calculate_valuation_score(
                ticker, fundamentals, eps_yoy, eps_3y, fcf_yield, market=args.market
            )
            
            # Calculate bonus points (0-15)
            from valuation_scorer import calculate_bonus_points
            bonus_points, bonus_details = calculate_bonus_points(ticker, info)
            
            # Add bonus to valuation score (capped at 100)
            val_score_with_bonus = min(100, val_score + bonus_points)
            
            tech_score, tech_details = calculate_technical_score(
                all_data['history'], spy_hist
            )
            
            # Composite score (use enhanced valuation score)
            composite_score = (val_score_with_bonus * VALUATION_WEIGHT) + (tech_score * TECHNICAL_WEIGHT)
            
            # Determine action (use enhanced valuation score for thresholds)
            action, emoji, needs_analysis, reasoning = get_action(val_score_with_bonus, tech_score, market_bullish)
            
            # ============================================================
            # 🎯 NEW: EXTENSION ANALYSIS (Only for BUY/STRONG_BUY)
            # ============================================================
            extension_data = None
            final_action = action
            final_emoji = emoji
            final_reasoning = reasoning
            
            if action in ['BUY', 'STRONG_BUY']:
                # Extract RSI from technical details
                rsi_value = tech_details.get('rsi', {})
                if isinstance(rsi_value, dict):
                    rsi = rsi_value.get('value', 50)
                else:
                    # Fallback: calculate RSI if not in proper format
                    from technical_scorer import calculate_rsi
                    rsi = calculate_rsi(all_data['history'])
                
                # Run extension analysis
                extension_data = classify_price_extension(
                    all_data['history'],
                    rsi,
                    tech_score
                )
                
                # Override action based on extension analysis
                ext_class = extension_data['classification']
                ext_risk = extension_data['risk_level']
                
                if ext_class == "EXTENDED":
                    final_action = "WATCH_EXTENDED"
                    final_emoji = "⚠️"
                    final_reasoning = extension_data['reasoning']
                    needs_analysis = False
                
                elif ext_class == "MOMENTUM":
                    final_action = f"{action}_MOMENTUM"
                    final_emoji = f"{emoji}⚡"
                    final_reasoning = extension_data['reasoning']
                
                elif ext_class == "EARLY_MOMENTUM":
                    final_action = f"{action}_EARLY_MOM"
                    final_emoji = f"{emoji}✅"
                    # Keep original reasoning but add confirmation
                    final_reasoning = f"{reasoning} | {extension_data['reasoning']}"
                
                else:  # EARLY - best entry
                    final_action = f"{action}_EARLY"
                    final_emoji = f"{emoji}💎"
                    final_reasoning = f"{reasoning} | {extension_data['reasoning']}"
            
            # ============================================================
            
            # Build result with extension data
            result = {
                # Basic Info
                'Ticker': ticker,
                'Sector': all_data['sector'],
                'Industry': all_data.get('industry', 'Unknown'),
                'Price': round(all_data['price'], 2),
                'Market Cap (M)': round(all_data['market_cap'] / 1_000_000, 0),
                
                # Scores
                'Valuation Score': round(val_score, 1),
                'Bonus Points': bonus_points,
                'Bonus Details': ', '.join(bonus_details) if bonus_details else 'None',
                'Enhanced Val Score': round(val_score_with_bonus, 1),
                'Technical Score': round(tech_score, 1),
                'Composite Score': round(composite_score, 1),
                
                # Action (potentially modified by extension analysis)
                'Action': final_action,
                'Priority': final_emoji,
                'Reasoning': final_reasoning,
                'Needs Deep Analysis': needs_analysis,
                
                # Extension Metrics (only populated for BUY/STRONG_BUY)
                'Extension Class': extension_data['classification'] if extension_data else 'N/A',
                'Risk Level': extension_data['risk_level'] if extension_data else 'N/A',
                'Rally 1M %': round(extension_data['metrics']['rally_1m'], 1) if extension_data else 0,
                'Rally 3M %': round(extension_data['metrics']['rally_3m'], 1) if extension_data else 0,
                'Rally 6M %': round(extension_data['metrics']['rally_6m'], 1) if extension_data else 0,
                'Dist from MA50 %': round(extension_data['metrics']['distance_from_50ma'], 1) if extension_data else 0,
                'Extension Score': extension_data['metrics']['extension_score'] if extension_data else 0,
                'Entry Guidance': ' | '.join(extension_data['entry_guidance']) if extension_data else 'N/A',
                
                # Key Metrics (for AI context)
                'PE Ratio': round(fundamentals.get('pe_ratio', 0), 2),
                'ROE': round(fundamentals.get('roe', 0), 2),
                'Debt/Equity': round(fundamentals.get('debt_equity', 0), 2),
                'Rev Growth %': round(fundamentals.get('revenue_growth', 0), 1),
                'Earnings Growth %': round(eps_yoy, 1),
                'RSI': round(rsi if extension_data else 0, 1),
                'MACD Bullish': tech_details.get('macd', {}).get('bullish', False) if isinstance(tech_details.get('macd'), dict) else False,
                'Above 50 MA': tech_details.get('trend', {}).get('above_ma50', False) if isinstance(tech_details.get('trend'), dict) else False,
                'Above 200 MA': tech_details.get('trend', {}).get('above_ma200', False) if isinstance(tech_details.get('trend'), dict) else False,
            }
            
            results.append(result)
            
            # Display with extension info for BUY/STRONG_BUY
            bonus_str = f" B:+{bonus_points}" if bonus_points > 0 else ""
            
            if extension_data:
                ext_info = f" [{extension_data['classification']}]"
                print(f"✅ V:{val_score:.0f}{bonus_str} T:{tech_score:.0f}{ext_info} → {final_action}")
            else:
                print(f"✅ V:{val_score:.0f}{bonus_str} T:{tech_score:.0f} → {final_action}")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    print()
    print("=" * 60)
    
    # Create DataFrame
    if not results:
        print("No stocks passed the filters!")
        return
    
    df = pd.DataFrame(results)
    
    # Sort by composite score
    df = df.sort_values('Composite Score', ascending=False)
    
    # Ensure output directory exists
    import os
    output_dir = os.path.dirname(OUTPUT_FILE)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Results saved to: {OUTPUT_FILE}")
    
    # Save JSON for AI analysis (Phase 2 preparation) - unless --no-json flag
    if not args.no_json:
        ai_candidates = df[df['Needs Deep Analysis'] == True]
        
        if len(ai_candidates) > 0:
            json_file = OUTPUT_FILE.replace('.csv', '_ai_queue.json')
            
            ai_data = {
                'scan_date': datetime.now().strftime('%Y-%m-%d'),
                'scan_time': datetime.now().strftime('%H:%M:%S'),
                'market': args.market.upper(),
                'market_regime': 'bullish' if market_bullish else 'bearish',
                'total_candidates': len(ai_candidates),
                'stocks': []
            }
            
            for _, stock in ai_candidates.iterrows():
                stock_context = {
                    'ticker': stock['Ticker'],
                    'action': stock['Action'],
                    'priority': 1 if 'STRONG_BUY' in stock['Action'] else 2,
                    'extension_class': stock['Extension Class'],
                    'risk_level': stock['Risk Level'],
                    'entry_guidance': stock['Entry Guidance'],
                    'scores': {
                        'composite': float(stock['Composite Score']),
                        'valuation': float(stock['Valuation Score']),
                        'technical': float(stock['Technical Score']),
                        'extension': int(stock['Extension Score'])
                    },
                    'rally_metrics': {
                        'rally_1m': float(stock['Rally 1M %']),
                        'rally_3m': float(stock['Rally 3M %']),
                        'rally_6m': float(stock['Rally 6M %'])
                    },
                    'fundamentals': {
                        'sector': stock['Sector'],
                        'industry': stock['Industry'],
                        'price': float(stock['Price']),
                        'market_cap_millions': float(stock['Market Cap (M)']),
                        'pe_ratio': float(stock['PE Ratio']),
                        'roe': float(stock['ROE']),
                        'debt_equity': float(stock['Debt/Equity']),
                        'revenue_growth': float(stock['Rev Growth %']),
                        'earnings_growth': float(stock['Earnings Growth %'])
                    },
                    'technicals': {
                        'rsi': float(stock['RSI']),
                        'macd_bullish': bool(stock['MACD Bullish']),
                        'above_ma50': bool(stock['Above 50 MA']),
                        'above_ma200': bool(stock['Above 200 MA'])
                    },
                    'reasoning': stock['Reasoning'],
                    'phase2_tasks': [
                        'Find recent news (last 7 days)',
                        'Analyze earnings sentiment',
                        'Check insider transactions',
                        'Assess competitive position',
                        'Evaluate growth catalysts',
                        'Identify risks',
                        'Validate extension analysis'
                    ]
                }
                ai_data['stocks'].append(stock_context)
            
            with open(json_file, 'w') as f:
                json.dump(ai_data, f, indent=2)
            
            print(f"✅ AI analysis queue saved to: {json_file}")
            print(f"   {len(ai_candidates)} stocks queued for Phase 2 deep analysis")
    
    print()
    
    # Display top picks with extension analysis
    print("TOP PICKS (WITH ENTRY TIMING ANALYSIS):")
    print("-" * 80)
    
    # Show STRONG BUY EARLY (optimal entries)
    early_strong = df[df['Action'].str.contains('STRONG_BUY_EARLY', na=False)]
    if not early_strong.empty:
        print("\n🔥🔥💎 STRONG BUY - OPTIMAL ENTRY (Best Risk/Reward):")
        display_cols = ['Ticker', 'Price', 'Enhanced Val Score', 'Technical Score', 'Extension Class', 'Rally 6M %', 'Entry Guidance']
        print(early_strong[display_cols].to_string(index=False))
    
    # Show STRONG BUY EARLY MOMENTUM
    early_mom_strong = df[df['Action'].str.contains('STRONG_BUY_EARLY_MOM', na=False)]
    if not early_mom_strong.empty:
        print("\n🔥🔥✅ STRONG BUY - EARLY MOMENTUM (Good Entry):")
        display_cols = ['Ticker', 'Price', 'Enhanced Val Score', 'Technical Score', 'Rally 1M %', 'Rally 3M %', 'Entry Guidance']
        print(early_mom_strong[display_cols].to_string(index=False))
    
    # Show regular BUY EARLY
    early_buys = df[df['Action'].str.contains('BUY_EARLY', na=False)]
    if not early_buys.empty:
        print("\n🔥💎 BUY - OPTIMAL ENTRY:")
        display_cols = ['Ticker', 'Price', 'Enhanced Val Score', 'Technical Score', 'Extension Class', 'Entry Guidance']
        print(early_buys[display_cols].to_string(index=False))
    
    # Show MOMENTUM plays (with caution)
    momentum = df[df['Action'].str.contains('MOMENTUM', na=False) & ~df['Action'].str.contains('EARLY_MOM', na=False)]
    if not momentum.empty:
        print("\n🔥⚡ BUY/STRONG_BUY - MOMENTUM (Proceed with Caution):")
        display_cols = ['Ticker', 'Price', 'Rally 1M %', 'Rally 3M %', 'Dist from MA50 %', 'Entry Guidance']
        print(momentum[display_cols].to_string(index=False))
    
    # Show EXTENDED (wait for pullback)
    extended = df[df['Action'] == 'WATCH_EXTENDED']
    if not extended.empty:
        print("\n⚠️ EXTENDED - WAIT FOR PULLBACK:")
        display_cols = ['Ticker', 'Price', 'Rally 6M %', 'Dist from MA50 %', 'RSI', 'Entry Guidance']   
        print(extended[display_cols].to_string(index=False))
    
    # If no strong signals, show top scored
    if (early_strong.empty and early_mom_strong.empty and early_buys.empty):
        print("\nNo optimal BUY/STRONG_BUY signals found. Top scored stocks:")
        print(df.head(10)[['Ticker', 'Action', 'Extension Class', 'Composite Score', 'Rally 6M %', 'Entry Guidance']])
    
    print()
    print("=" * 80)
    print("SUMMARY:")
    print(f"Total Scanned: {len(STOCK_UNIVERSE)}")
    print(f"Passed Filters: {len(df)}")
    print(f"STRONG BUY - Optimal Entry: {len(early_strong)} 🔥🔥💎")
    print(f"STRONG BUY - Early Momentum: {len(early_mom_strong)} 🔥🔥✅")
    print(f"BUY - Optimal Entry: {len(early_buys)} 🔥💎")
    print(f"BUY/STRONG_BUY - Momentum: {len(momentum)} 🔥⚡ (Higher Risk)")
    print(f"EXTENDED - Wait for Pullback: {len(extended)} ⚠️")
    print(f"WATCH Signals: {len(df[df['Action'] == 'WATCH'])} ⏳")
    print(f"WAIT Signals: {len(df[df['Action'] == 'WAIT'])} 🕐")
    print()
    print(f"Stocks Queued for Phase 2 AI Analysis: {len(df[df['Needs Deep Analysis'] == True])}")
    print("=" * 80)
    
    print("\n💡 TIP: Prioritize stocks with 'OPTIMAL ENTRY' or 'EARLY MOMENTUM' classifications")
    print("         for best risk/reward. Avoid 'EXTENDED' stocks until they pull back.")

if __name__ == "__main__":
    main()