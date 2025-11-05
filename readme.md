# Hidden Gems Stock Screener

A simple Python tool to find undervalued quality stocks using fundamental analysis (valuation) and technical analysis (timing).

## Setup (Windows)

### 1. Install Python
- Download Python 3.10+ from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

### 2. Install Dependencies
Open Command Prompt (cmd) and run:
```
cd path\to\this\folder
pip install -r requirements.txt
```

### 3. Customize Stock Universe
- Edit `config.py`
- Update `STOCK_UNIVERSE` list with tickers you want to scan
- Default includes 230+ small/mid-cap stocks across all sectors

## Usage

Run the screener:
```
python main.py
```

The script will:
1. Check market conditions (SPY 200 MA filter)
2. Scan all stocks in your universe
3. Apply filters (market cap, volume)
4. Calculate valuation scores (fundamentals)
5. Calculate technical scores (timing)
6. Generate composite scores
7. Output results to `stock_picks.csv`

**Runtime:** ~5-10 minutes for 230 stocks (no API delays!)

## Output

`stock_picks.csv` contains:
- Ticker, Sector, Price
- Valuation Score (0-100)
- Technical Score (0-100)
- Composite Score (weighted average)
- Action: BUY / WATCH / WAIT / AVOID / SPECULATIVE / CASH
- Key metrics: P/E, ROE, Debt/Equity, Revenue Growth, Earnings Growth

## What Each Action Means

- **BUY 🔥**: High valuation + high technical = strong buy signal
- **WATCH ⏳**: Good fundamentals, neutral technicals = monitor
- **WAIT 🕐**: Great company, bad timing = wait for entry
- **SPECULATIVE ⚠️**: Okay fundamentals, strong momentum = risky
- **AVOID ❌**: Weak fundamentals or technicals
- **CASH 💰**: Market bearish (SPY below 200 MA)

## Customization

Edit `config.py` to adjust:
- Market cap range (default: $300M - $10B)
- Volume thresholds (default: >500K avg volume)
- Valuation scoring weights
- Technical indicator parameters
- Number of top stocks to show

## Data Source

**100% Yahoo Finance** - No API key needed!
- Free unlimited usage
- Real-time data
- Comprehensive fundamental metrics
- Historical price data for technical analysis

## Important Notes

1. **No API Limits**: Yahoo Finance through yfinance is free and unlimited

2. **Data Quality**: Yahoo Finance has excellent coverage for US stocks
   - Most stocks will have complete fundamental data
   - Technical data available for all liquid stocks

3. **Not Financial Advice**: This is a screening tool only
   - Always do your own research
   - Consider risk management and position sizing
   - Past performance ≠ future results

## Troubleshooting

**"No module named 'yfinance'"**
- Run: `pip install -r requirements.txt`

**"No stocks passed filters"**
- Many stocks in your universe may be too large (>$10B)
- Edit `config.py` to relax MARKET_CAP_MAX to 50B
- Or add more small-cap tickers to STOCK_UNIVERSE

**Scores are low**
- Growth stocks without profits score lower on valuation
- Check SPECULATIVE category for momentum plays
- Consider adjusting scoring weights in config.py

## Next Steps

Phase 2 (Future):
- Indian stocks (NSE)
- Email alerts
- GitHub automation
- AI/LLM enhancements
- Agentic workflow