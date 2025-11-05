import pandas as pd
import yfinance as yf
from datetime import datetime
from config import *
from data_fetcher import get_stock_data, get_fundamentals, get_earnings_growth, get_fcf_yield
from valuation_scorer import calculate_valuation_score
from technical_scorer import calculate_technical_score

def check_market_filter():
    """Check if SPY is above 200 MA"""
    spy = yf.Ticker('SPY')
    spy_hist = spy.history(period='1y')
    
    if len(spy_hist) < 200:
        return False, spy_hist
    
    sma_200 = spy_hist['Close'].rolling(window=200).mean().iloc[-1]
    current_price = spy_hist['Close'].iloc[-1]
    
    return current_price > sma_200, spy_hist

def apply_filters(stock_data):
    """Apply hidden gems filters"""
    
    # Market Cap Filter
    if not (MARKET_CAP_MIN <= stock_data['market_cap'] <= MARKET_CAP_MAX):
        return False, f"Market cap ${stock_data['market_cap']/1e9:.1f}B (need $0.3B-$10B)"
    
    # Volume Filter
    if stock_data['avg_volume'] < MIN_AVG_VOLUME:
        return False, f"Volume {stock_data['avg_volume']:,.0f} (need >500K)"
    
    return True, "Passed"

def get_action(val_score, tech_score, market_bullish):
    """Determine action based on scores"""
    
    if not market_bullish:
        return "CASH", "💰"
    
    if val_score > 70 and tech_score > 60:
        return "BUY", "🔥"
    elif val_score > 70 and 40 <= tech_score <= 60:
        return "WATCH", "⏳"
    elif val_score > 70 and tech_score < 40:
        return "WAIT", "🕐"
    elif 50 <= val_score <= 70 and tech_score > 60:
        return "SPECULATIVE", "⚠️"
    else:
        return "AVOID", "❌"

def main():
    print("=" * 60)
    print("HIDDEN GEMS STOCK SCREENER")
    print("=" * 60)
    print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data Source: Yahoo Finance (No API limits!)")
    print()
    
    # Check market filter
    print("Checking market conditions (SPY 200 MA)...")
    market_bullish, spy_hist = check_market_filter()
    print(f"Market Status: {'🟢 BULLISH' if market_bullish else '🔴 BEARISH'}")
    print()
    
    results = []
    
    print(f"Scanning {len(STOCK_UNIVERSE)} stocks...")
    print("-" * 60)
    
    for i, ticker in enumerate(STOCK_UNIVERSE, 1):
        print(f"[{i}/{len(STOCK_UNIVERSE)}] {ticker}...", end=" ")
        
        try:
            # Get stock data
            stock_data = get_stock_data(ticker)
            if not stock_data:
                print("❌ No data")
                continue
            
            # Apply filters
            passed, reason = apply_filters(stock_data)
            if not passed:
                print(f"❌ {reason}")
                continue
            
            # Get fundamentals (from same Yahoo Finance call)
            stock = yf.Ticker(ticker)
            info = stock.info
            fundamentals = get_fundamentals(ticker)
            
            if not fundamentals:
                print("❌ No fundamentals")
                continue
            
            # Get earnings growth
            eps_yoy, eps_3y = get_earnings_growth(ticker, info)
            
            # Get FCF yield
            fcf_yield = get_fcf_yield(ticker, stock_data['market_cap'], info)
            
            # Calculate scores
            val_score, val_details = calculate_valuation_score(
                ticker, fundamentals, eps_yoy, eps_3y, fcf_yield
            )
            
            tech_score, tech_details = calculate_technical_score(
                stock_data['history'], spy_hist
            )
            
            # Composite score
            composite_score = (val_score * VALUATION_WEIGHT) + (tech_score * TECHNICAL_WEIGHT)
            
            # Determine action
            action, emoji = get_action(val_score, tech_score, market_bullish)
            
            results.append({
                'Ticker': ticker,
                'Sector': stock_data['sector'],
                'Price': round(stock_data['price'], 2),
                'Market Cap (M)': round(stock_data['market_cap'] / 1_000_000, 0),
                'Valuation Score': round(val_score, 1),
                'Technical Score': round(tech_score, 1),
                'Composite Score': round(composite_score, 1),
                'Action': action,
                'Priority': emoji,
                'PE Ratio': round(fundamentals.get('pe_ratio', 0), 2),
                'ROE': round(fundamentals.get('roe', 0), 2),
                'Debt/Equity': round(fundamentals.get('debt_equity', 0), 2),
                'Rev Growth %': round(fundamentals.get('revenue_growth', 0), 1),
                'Earnings Growth %': round(eps_yoy, 1),
            })
            
            print(f"✅ V:{val_score:.0f} T:{tech_score:.0f} → {action}")
            
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
    
    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Results saved to: {OUTPUT_FILE}")
    print()
    
    # Display top picks
    print("TOP PICKS:")
    print("-" * 60)
    top_picks = df[df['Action'] == 'BUY'].head(TOP_N_STOCKS)
    
    if top_picks.empty:
        print("No BUY signals found. Top scored stocks:")
        print(df.head(10)[['Ticker', 'Action', 'Composite Score', 'Valuation Score', 'Technical Score', 'Price']])
    else:
        print(top_picks[['Ticker', 'Action', 'Priority', 'Composite Score', 'Valuation Score', 'Technical Score', 'Price']])
    
    print()
    print("=" * 60)
    print("SUMMARY:")
    print(f"Total Scanned: {len(STOCK_UNIVERSE)}")
    print(f"Passed Filters: {len(df)}")
    print(f"BUY Signals: {len(df[df['Action'] == 'BUY'])}")
    print(f"WATCH Signals: {len(df[df['Action'] == 'WATCH'])}")
    print(f"SPECULATIVE Signals: {len(df[df['Action'] == 'SPECULATIVE'])}")
    print("=" * 60)

if __name__ == "__main__":
    main()