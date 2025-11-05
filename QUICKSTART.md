# 🚀 Quick Start Guide

## ✅ What You Have Now

A complete, production-ready stock screener with:
- ✅ Clean folder structure
- ✅ GitHub automation ready
- ✅ Daily scheduled scans
- ✅ Proper documentation
- ✅ Simple to use

---

## 📁 Folder Structure

```
hidden-gems-screener/
│
├── src/                          # Source code
│   ├── config.py                # Settings & stock universe
│   ├── main.py                  # Main screener
│   ├── data_fetcher.py          # Yahoo Finance data
│   ├── valuation_scorer.py      # Fundamental scoring
│   └── technical_scorer.py      # Technical scoring
│
├── output/                       # Results folder
│   ├── stock_picks.csv          # Latest results
│   └── stock_picks_YYYYMMDD.csv # Historical scans
│
├── docs/                         # Documentation
│   └── GITHUB_SETUP.md          # GitHub instructions
│
├── .github/workflows/            # GitHub Actions
│   └── daily-scan.yml           # Automation workflow
│
├── README.md                     # Main documentation
├── requirements.txt              # Python packages
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT license
└── run.bat                       # Windows quick run
```

---

## 🖥️ Local Usage (Windows)

### Method 1: Double-Click (Easiest)
1. Double-click `run.bat`
2. Wait 5-10 minutes
3. Check `output/stock_picks.csv`

### Method 2: Command Line
```bash
cd src
python main.py
```

---

## 🤖 GitHub Automation Setup

### Step 1: Create GitHub Repo
```bash
# In your project folder
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hidden-gems-screener.git
git push -u origin main
```

### Step 2: Enable Actions
1. Go to your repo on GitHub
2. Click "Actions" tab
3. Actions are auto-enabled

### Step 3: Test It
1. Go to Actions tab
2. Click "Daily Stock Screener"
3. Click "Run workflow" → Run
4. Wait 5-10 minutes
5. Check `output/` folder for results

### Step 4: Enjoy Daily Automation
- Runs automatically every weekday at 5 PM EST
- Results auto-commit to repo
- View history in `output/` folder

---

## 📊 Understanding Results

### CSV Columns
- **Ticker** - Stock symbol
- **Sector** - Industry sector
- **Price** - Current price
- **Market Cap** - Company size
- **Valuation Score** (0-100) - Fundamental quality
- **Technical Score** (0-100) - Timing quality
- **Composite Score** - Weighted average (60% val + 40% tech)
- **Action** - BUY / WATCH / WAIT / SPECULATIVE / AVOID / CASH

### Action Signals
- **🔥 BUY** - High quality + perfect timing → Top conviction
- **⏳ WATCH** - Good fundamentals, waiting for entry
- **🕐 WAIT** - Great company, wrong timing
- **⚠️ SPECULATIVE** - Momentum play, higher risk
- **❌ AVOID** - Weak fundamentals or technicals
- **💰 CASH** - Market bearish (SPY < 200 MA)

---

## 🎛️ Customization

### Change Stock Universe
Edit `src/config.py`:
```python
STOCK_UNIVERSE = [
    'YOUR', 'CUSTOM', 'TICKERS', 'HERE'
]
```

### Adjust Filters
```python
MARKET_CAP_MIN = 300_000_000   # $300M
MARKET_CAP_MAX = 10_000_000_000 # $10B
MIN_AVG_VOLUME = 500_000        # 500K shares/day
```

### Change Schedule
Edit `.github/workflows/daily-scan.yml`:
```yaml
schedule:
  - cron: '0 21 * * 1-5'  # 5 PM EST, Mon-Fri
```

Cron examples:
- `0 22 * * 1-5` = 6 PM EST
- `0 14 * * 1-5` = 10 AM EST
- `30 20 * * 1-5` = 4:30 PM EST

---

## 🔧 Troubleshooting

### "No stocks passed filters"
- Your universe may have mostly large-cap stocks
- Edit `config.py` → increase `MARKET_CAP_MAX` to 50B
- Or add more small-cap tickers

### "Low scores / No BUY signals"
- Normal! System is selective (not every stock is a buy)
- Check WATCH and SPECULATIVE signals
- Run during different market conditions

### GitHub Action fails
- Check Actions tab → click failed run → view logs
- Usually a permissions issue (auto-fixes on retry)

---

## 📈 Next Phase Ideas

Once you're comfortable with the basics:

### Phase 2A: Email Alerts
- Send top 5 picks to your email daily
- Uses GitHub Actions + email service

### Phase 2B: Indian Stocks (NSE)
- Adapt for BSE/NSE tickers
- Different data sources (NSE API)

### Phase 2C: AI Enhancement
- Add sentiment analysis (news/earnings calls)
- LLM-based qualitative scoring
- Agentic workflow for deeper analysis

**Want any of these?** Let me know!

---

## ⚠️ Important Notes

1. **Not Financial Advice** - This is a screening tool only
2. **Do Your Research** - Always verify before investing
3. **Risk Management** - Use proper position sizing
4. **Backtesting** - Track results to validate the system
5. **Paper Trade First** - Test picks with fake money

---

## 🎯 Success Metrics

Track these over time:
- Win rate (% of BUY signals that work)
- Average return per signal
- Max drawdown
- Time to exit (avg holding period)

**Good system:** 60%+ win rate, 15%+ avg return

---

## 📞 Support

- **Issues?** Check `docs/GITHUB_SETUP.md`
- **Questions?** Open a GitHub issue
- **Improvements?** PRs welcome!

---

**Happy hunting for hidden gems!** 💎🚀