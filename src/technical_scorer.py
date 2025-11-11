import pandas as pd
import numpy as np
from src.config import *

def calculate_sma(data, period):
    """Simple Moving Average"""
    return data['Close'].rolling(window=period).mean()

def calculate_rsi(data, period=14):
    """Relative Strength Index"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def calculate_macd(data):
    """MACD Indicator"""
    exp1 = data['Close'].ewm(span=MACD_FAST, adjust=False).mean()
    exp2 = data['Close'].ewm(span=MACD_SLOW, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=MACD_SIGNAL, adjust=False).mean()
    histogram = macd - signal
    
    return {
        'macd': macd.iloc[-1],
        'signal': signal.iloc[-1],
        'histogram': histogram.iloc[-1],
        'histogram_prev': histogram.iloc[-2]
    }

def calculate_adx(data, period=14):
    """Average Directional Index"""
    high = data['High']
    low = data['Low']
    close = data['Close']
    
    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    
    tr = pd.DataFrame()
    tr['h-l'] = high - low
    tr['h-pc'] = abs(high - close.shift(1))
    tr['l-pc'] = abs(low - close.shift(1))
    tr['tr'] = tr[['h-l', 'h-pc', 'l-pc']].max(axis=1)
    
    atr = tr['tr'].rolling(window=period).mean()
    plus_di = 100 * (plus_dm.ewm(alpha=1/period).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha=1/period).mean() / atr))
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    adx = dx.ewm(alpha=1/period).mean()
    
    return adx.iloc[-1] if not adx.empty else 0

def calculate_technical_score(data, spy_data):
    """Calculate technical score (0-100)"""
    
    if data.empty or len(data) < 200:
        return 0, {}
    
    score = 0
    details = {}
    
    # 1. Trend (MA) - 1 point
    sma_50 = calculate_sma(data, 50).iloc[-1]
    sma_200 = calculate_sma(data, 200).iloc[-1]
    current_price = data['Close'].iloc[-1]
    
    if current_price > sma_50 and sma_50 > sma_200:
        score += 1.0
        details['trend'] = 'Strong'
    elif current_price > sma_50 or sma_50 > sma_200:
        score += 0.5
        details['trend'] = 'Moderate'
    else:
        details['trend'] = 'Weak'
    
    # 2. Volume Trend - 1 point
    vol_20 = data['Volume'].tail(20).mean()
    vol_50 = data['Volume'].tail(50).mean()
    
    if vol_20 > vol_50:
        score += 1.0
        details['volume'] = 'Increasing'
    elif vol_20 > vol_50 * 0.9:
        score += 0.5
        details['volume'] = 'Stable'
    else:
        details['volume'] = 'Decreasing'
    
    # 3. RSI - 1 point
    rsi = calculate_rsi(data, RSI_PERIOD)
    if 40 <= rsi <= 60:
        score += 1.0
        details['rsi'] = 'Healthy'
    elif 30 <= rsi <= 70:
        score += 0.5
        details['rsi'] = 'Acceptable'
    else:
        details['rsi'] = 'Extreme'
    
    # 4. MACD - 1 point
    macd_data = calculate_macd(data)
    if macd_data['macd'] > macd_data['signal'] and macd_data['histogram'] > macd_data['histogram_prev']:
        score += 1.0
        details['macd'] = 'Bullish'
    elif macd_data['macd'] > macd_data['signal'] or macd_data['histogram'] > macd_data['histogram_prev']:
        score += 0.5
        details['macd'] = 'Neutral'
    else:
        details['macd'] = 'Bearish'
    
    # 5. Relative Strength vs SPY - 1 point
    stock_return = (data['Close'].iloc[-1] / data['Close'].iloc[-60] - 1) * 100
    spy_return = (spy_data['Close'].iloc[-1] / spy_data['Close'].iloc[-60] - 1) * 100
    
    if stock_return > spy_return:
        score += 1.0
        details['rel_strength'] = 'Outperforming'
    elif stock_return > spy_return * 0.9:
        score += 0.5
        details['rel_strength'] = 'Matching'
    else:
        details['rel_strength'] = 'Underperforming'
    
    # 6. Price vs 52W High - 1 point
    high_52w = data['High'].tail(252).max()
    pct_from_high = ((current_price / high_52w) - 1) * 100
    
    if pct_from_high >= -20:
        score += 1.0
        details['price_position'] = 'Near High'
    elif pct_from_high >= -40:
        score += 0.5
        details['price_position'] = 'Mid Range'
    else:
        details['price_position'] = 'Far from High'
    
    # 7. ADX (Trend Strength) - 1 point
    adx = calculate_adx(data, ADX_PERIOD)
    if adx > 25:
        score += 1.0
        details['adx'] = 'Strong Trend'
    elif adx > 20:
        score += 0.5
        details['adx'] = 'Developing'
    else:
        details['adx'] = 'Weak Trend'
    
    # Convert to 0-100 scale
    score_normalized = (score / 7) * 100
    
    return score_normalized, details