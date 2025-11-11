from config import *

def calculate_valuation_score(ticker, fundamentals, eps_yoy, eps_3y, fcf_yield, sector_pe_avg=20, market="US"):
    """
    Calculate weighted valuation score (0-100)
    
    Args:
        ticker: Stock ticker
        fundamentals: Fundamental metrics dict
        eps_yoy: YoY EPS growth
        eps_3y: 3Y EPS CAGR
        fcf_yield: Free cash flow yield
        sector_pe_avg: Sector average P/E
        market: "US", "INDIA", or "BOTH" - determines which thresholds to use
    
    Returns:
        Tuple of (score, details_dict)
    """
    
    if not fundamentals:
        return 0, {}
    
    # Select thresholds based on market
    # For Indian stocks (.NS or .BO suffix) or when market is INDIA, use India thresholds
    is_indian_stock = ticker.endswith('.NS') or ticker.endswith('.BO') or market == "INDIA"
    
    if is_indian_stock:
        # Use India-specific thresholds
        eps_growth_exc = INDIA_EPS_GROWTH_EXCELLENT
        eps_growth_good = INDIA_EPS_GROWTH_GOOD
        eps_3y_exc = INDIA_EPS_GROWTH_3Y_EXCELLENT
        eps_3y_good = INDIA_EPS_GROWTH_3Y_GOOD
        roe_exc = INDIA_ROE_EXCELLENT
        roe_good = INDIA_ROE_GOOD
        de_exc = INDIA_DEBT_EQUITY_EXCELLENT
        de_good = INDIA_DEBT_EQUITY_GOOD
        pe_sector_exc = INDIA_PE_SECTOR_EXCELLENT
        pe_sector_good = INDIA_PE_SECTOR_GOOD
        peg_exc = INDIA_PEG_EXCELLENT
        peg_good = INDIA_PEG_GOOD
        fcf_exc = INDIA_FCF_YIELD_EXCELLENT
        fcf_good = INDIA_FCF_YIELD_GOOD
    else:
        # Use US/Global thresholds
        eps_growth_exc = EPS_GROWTH_EXCELLENT
        eps_growth_good = EPS_GROWTH_GOOD
        eps_3y_exc = EPS_GROWTH_3Y_EXCELLENT
        eps_3y_good = EPS_GROWTH_3Y_GOOD
        roe_exc = ROE_EXCELLENT
        roe_good = ROE_GOOD
        de_exc = DEBT_EQUITY_EXCELLENT
        de_good = DEBT_EQUITY_GOOD
        pe_sector_exc = PE_SECTOR_EXCELLENT
        pe_sector_good = PE_SECTOR_GOOD
        peg_exc = PEG_EXCELLENT
        peg_good = PEG_GOOD
        fcf_exc = FCF_YIELD_EXCELLENT
        fcf_good = FCF_YIELD_GOOD
    
    score = 0
    details = {}
    
    # 1. EPS Growth YoY (25 points)
    if eps_yoy:
        if eps_yoy >= eps_growth_exc:
            score += 25
            details['eps_yoy'] = 'Excellent'
        elif eps_yoy >= eps_growth_good:
            score += 15
            details['eps_yoy'] = 'Good'
        else:
            score += 5
            details['eps_yoy'] = 'Poor'
    
    # 2. EPS Growth 3Y CAGR (15 points)
    if eps_3y:
        if eps_3y >= eps_3y_exc:
            score += 15
            details['eps_3y'] = 'Excellent'
        elif eps_3y >= eps_3y_good:
            score += 10
            details['eps_3y'] = 'Good'
        else:
            score += 3
            details['eps_3y'] = 'Poor'
    
    # 3. ROE (20 points)
    roe = fundamentals.get('roe', 0)
    if roe >= roe_exc:
        score += 20
        details['roe'] = 'Excellent'
    elif roe >= roe_good:
        score += 12
        details['roe'] = 'Good'
    else:
        score += 5
        details['roe'] = 'Poor'
    
    # 4. Debt/Equity (15 points)
    de = fundamentals.get('debt_equity', 999)
    if de <= de_exc:
        score += 15
        details['debt_equity'] = 'Excellent'
    elif de <= de_good:
        score += 10
        details['debt_equity'] = 'Good'
    else:
        score += 3
        details['debt_equity'] = 'Poor'
    
    # 5. P/E vs Sector (10 points)
    pe = fundamentals.get('pe_ratio', 0)
    if pe > 0 and sector_pe_avg > 0:
        pe_ratio = pe / sector_pe_avg
        if pe_ratio <= pe_sector_exc:
            score += 10
            details['pe_sector'] = 'Excellent'
        elif pe_ratio <= pe_sector_good:
            score += 6
            details['pe_sector'] = 'Good'
        else:
            score += 2
            details['pe_sector'] = 'Poor'
    
    # 6. PEG Ratio (10 points)
    peg = fundamentals.get('peg_ratio', 999)
    if peg > 0:
        if peg <= peg_exc:
            score += 10
            details['peg'] = 'Excellent'
        elif peg <= peg_good:
            score += 6
            details['peg'] = 'Good'
        else:
            score += 2
            details['peg'] = 'Poor'
    
    # 7. FCF Yield (5 points)
    if fcf_yield >= fcf_exc:
        score += 5
        details['fcf_yield'] = 'Excellent'
    elif fcf_yield >= fcf_good:
        score += 3
        details['fcf_yield'] = 'Good'
    else:
        score += 1
        details['fcf_yield'] = 'Poor'
    
    return score, details

def calculate_bonus_points(ticker, info):
    """
    Calculate optional bonus points (0-15) for quality signals
    Philosophy: Each bonus is independent - stock doesn't need all three
    
    Args:
        ticker: Stock ticker
        info: Yahoo Finance info dict
    
    Returns:
        Tuple of (bonus_points, bonus_details)
    """
    bonus = 0
    details = []
    
    try:
        # Bonus 1: Low Short Interest (+5 if market shows confidence)
        short_pct = info.get('shortPercentOfFloat', None)
        if short_pct is not None:
            short_pct_display = short_pct * 100
            if short_pct_display > 0 and short_pct_display < SHORT_INTEREST_THRESHOLD:
                bonus += SHORT_INTEREST_BONUS
                details.append(f"Low shorts ({short_pct_display:.1f}%)")
    except:
        pass  # No penalty if data unavailable
    
    try:
        # Bonus 2: Institutional Interest (+5 if smart money interested)
        inst_pct = info.get('heldPercentInstitutions', None)
        if inst_pct is not None:
            inst_pct_display = inst_pct * 100
            if inst_pct_display >= INSTITUTIONAL_THRESHOLD:
                bonus += INSTITUTIONAL_BONUS
                details.append(f"Institutions ({inst_pct_display:.1f}%)")
    except:
        pass
    
    try:
        # Bonus 3: Insider Buying (+5 if insiders buying)
        # Try to get insider transactions from yfinance
        import yfinance as yf
        stock = yf.Ticker(ticker)
        
        # Get insider transactions if available
        try:
            insider_df = stock.insider_transactions
            if insider_df is not None and len(insider_df) > 0:
                # Count purchases in last 3 months
                import pandas as pd
                from datetime import datetime, timedelta
                
                three_months_ago = datetime.now() - timedelta(days=90)
                insider_df['Start Date'] = pd.to_datetime(insider_df['Start Date'])
                recent = insider_df[insider_df['Start Date'] >= three_months_ago]
                
                # Count buy transactions (positive shares or "Purchase" in transaction)
                buys = recent[
                    (recent['Shares'] > 0) | 
                    (recent['Transaction'].str.contains('Purchase', case=False, na=False))
                ]
                
                if len(buys) >= INSIDER_BUY_THRESHOLD:
                    bonus += INSIDER_BUY_BONUS
                    details.append(f"Insider buying ({len(buys)} txns)")
        except:
            pass  # Insider data not available - no penalty
    except:
        pass
    
    return bonus, details