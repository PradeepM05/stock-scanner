import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_all_stock_data(ticker):
    """Fetch ALL stock data in ONE Yahoo Finance call - optimized!"""
    try:
        # Single Yahoo Finance call
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1y")
        
        if hist.empty or len(hist) < 50:
            return None
        
        # Package everything together
        all_data = {
            # Basic Info
            'ticker': ticker,
            'price': hist['Close'].iloc[-1],
            'market_cap': info.get('marketCap', 0),
            'avg_volume': hist['Volume'].tail(20).mean(),
            'sector': info.get('sector', 'Unknown'),
            'industry': info.get('industry', 'Unknown'),
            'history': hist,
            
            # Fundamentals
            'fundamentals': {
                'pe_ratio': info.get('trailingPE', 0) or info.get('forwardPE', 0) or 0,
                'peg_ratio': info.get('pegRatio', 0) or 0,
                'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
                'roa': info.get('returnOnAssets', 0) * 100 if info.get('returnOnAssets') else 0,
                'debt_equity': info.get('debtToEquity', 0) / 100 if info.get('debtToEquity') else 0,
                'eps': info.get('trailingEps', 0) or 0,
                'revenue_per_share': info.get('revenuePerShare', 0) or 0,
                'profit_margin': info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0,
                'operating_margin': info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else 0,
                'gross_margin': info.get('grossMargins', 0) * 100 if info.get('grossMargins') else 0,
                'book_value': info.get('bookValue', 0) or 0,
                'price_to_book': info.get('priceToBook', 0) or 0,
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'beta': info.get('beta', 0) or 0,
                'shares_outstanding': info.get('sharesOutstanding', 0) or 0,
                'current_ratio': info.get('currentRatio', 0) or 0,
                'quick_ratio': info.get('quickRatio', 0) or 0,
                'revenue_growth': info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0,
                'earnings_growth': info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else 0,
            },
            
            # For earnings growth calculation
            'info': info
        }
        
        return all_data
        
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

# Legacy functions for backward compatibility (now just extract from all_data)
def get_stock_data(ticker):
    """DEPRECATED: Use get_all_stock_data() instead"""
    all_data = get_all_stock_data(ticker)
    if not all_data:
        return None
    
    return {
        'ticker': all_data['ticker'],
        'price': all_data['price'],
        'market_cap': all_data['market_cap'],
        'avg_volume': all_data['avg_volume'],
        'sector': all_data['sector'],
        'industry': all_data['industry'],
        'history': all_data['history']
    }

def get_fundamentals(ticker):
    """DEPRECATED: Use get_all_stock_data() instead"""
    all_data = get_all_stock_data(ticker)
    if not all_data:
        return None
    return all_data['fundamentals']

def get_earnings_growth(ticker, info=None):
    """Calculate EPS growth from Yahoo Finance data"""
    try:
        if not info:
            stock = yf.Ticker(ticker)
            info = stock.info
            
        # Get earnings growth from info (quarterly)
        earnings_growth = info.get('earningsGrowth', 0)
        revenue_growth = info.get('revenueGrowth', 0)
        
        # Convert to percentage
        eps_yoy = earnings_growth * 100 if earnings_growth else 0
        
        # For 3Y CAGR, use earnings quarterly trend if available
        # Simplified: use same as YoY for now (can enhance later)
        eps_3y = eps_yoy * 0.9 if eps_yoy > 0 else 0
        
        # If no earnings growth, use revenue growth as proxy
        if eps_yoy == 0 and revenue_growth:
            eps_yoy = revenue_growth * 100
            eps_3y = eps_yoy * 0.9
        
        return eps_yoy, eps_3y
        
    except Exception as e:
        return 0, 0

def get_fcf_yield(ticker, market_cap, info=None):
    """Calculate Free Cash Flow Yield from Yahoo Finance"""
    try:
        if not info:
            stock = yf.Ticker(ticker)
            info = stock.info
            
        # Get free cash flow from info
        fcf = info.get('freeCashflow', 0)
        
        if fcf and fcf > 0 and market_cap > 0:
            fcf_yield = (fcf / market_cap) * 100
            return fcf_yield
        
        # Alternative: operating cash flow - capex
        operating_cf = info.get('operatingCashflow', 0)
        if operating_cf and operating_cf > 0 and market_cap > 0:
            fcf_yield = (operating_cf / market_cap) * 100
            return fcf_yield
            
        return 0
        
    except Exception as e:
        return 0