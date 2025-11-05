from config import *

def calculate_valuation_score(ticker, fundamentals, eps_yoy, eps_3y, fcf_yield, sector_pe_avg=20):
    """Calculate weighted valuation score (0-100)"""
    
    if not fundamentals:
        return 0, {}
    
    score = 0
    details = {}
    
    # 1. EPS Growth YoY (25 points)
    if eps_yoy:
        if eps_yoy >= EPS_GROWTH_EXCELLENT:
            score += 25
            details['eps_yoy'] = 'Excellent'
        elif eps_yoy >= EPS_GROWTH_GOOD:
            score += 15
            details['eps_yoy'] = 'Good'
        else:
            score += 5
            details['eps_yoy'] = 'Poor'
    
    # 2. EPS Growth 3Y CAGR (15 points)
    if eps_3y:
        if eps_3y >= EPS_GROWTH_3Y_EXCELLENT:
            score += 15
            details['eps_3y'] = 'Excellent'
        elif eps_3y >= EPS_GROWTH_3Y_GOOD:
            score += 10
            details['eps_3y'] = 'Good'
        else:
            score += 3
            details['eps_3y'] = 'Poor'
    
    # 3. ROE (20 points)
    roe = fundamentals.get('roe', 0)
    if roe >= ROE_EXCELLENT:
        score += 20
        details['roe'] = 'Excellent'
    elif roe >= ROE_GOOD:
        score += 12
        details['roe'] = 'Good'
    else:
        score += 5
        details['roe'] = 'Poor'
    
    # 4. Debt/Equity (15 points)
    de = fundamentals.get('debt_equity', 999)
    if de <= DEBT_EQUITY_EXCELLENT:
        score += 15
        details['debt_equity'] = 'Excellent'
    elif de <= DEBT_EQUITY_GOOD:
        score += 10
        details['debt_equity'] = 'Good'
    else:
        score += 3
        details['debt_equity'] = 'Poor'
    
    # 5. P/E vs Sector (10 points)
    pe = fundamentals.get('pe_ratio', 0)
    if pe > 0 and sector_pe_avg > 0:
        pe_ratio = pe / sector_pe_avg
        if pe_ratio <= PE_SECTOR_EXCELLENT:
            score += 10
            details['pe_sector'] = 'Excellent'
        elif pe_ratio <= PE_SECTOR_GOOD:
            score += 6
            details['pe_sector'] = 'Good'
        else:
            score += 2
            details['pe_sector'] = 'Poor'
    
    # 6. PEG Ratio (10 points)
    peg = fundamentals.get('peg_ratio', 999)
    if peg > 0:
        if peg <= PEG_EXCELLENT:
            score += 10
            details['peg'] = 'Excellent'
        elif peg <= PEG_GOOD:
            score += 6
            details['peg'] = 'Good'
        else:
            score += 2
            details['peg'] = 'Poor'
    
    # 7. FCF Yield (5 points)
    if fcf_yield >= FCF_YIELD_EXCELLENT:
        score += 5
        details['fcf_yield'] = 'Excellent'
    elif fcf_yield >= FCF_YIELD_GOOD:
        score += 3
        details['fcf_yield'] = 'Good'
    else:
        score += 1
        details['fcf_yield'] = 'Poor'
    
    return score, details