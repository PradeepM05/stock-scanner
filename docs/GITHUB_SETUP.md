# GitHub Setup Instructions

## 1. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `hidden-gems-screener`
3. Description: "Automated stock screener for finding undervalued quality stocks"
4. Public or Private (your choice)
5. **Don't** initialize with README (we have one)
6. Click "Create repository"

## 2. Push Your Code

Open Command Prompt in your project folder and run:

```bash
git init
git add .
git commit -m "Initial commit: Hidden Gems Stock Screener"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hidden-gems-screener.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## 3. Enable GitHub Actions

1. Go to your repo on GitHub
2. Click "Actions" tab
3. GitHub Actions should be enabled by default
4. You'll see "Daily Stock Screener" workflow

## 4. Test the Automation

### Option A: Wait for Scheduled Run
- Workflow runs automatically every weekday at 5 PM EST

### Option B: Trigger Manually (Recommended First Time)
1. Go to "Actions" tab
2. Click "Daily Stock Screener" workflow
3. Click "Run workflow" button
4. Select branch: `main`
5. Click green "Run workflow" button

Wait 5-10 minutes, then check:
- "Actions" tab → see if run succeeded (green checkmark)
- `output/` folder → new CSV file should appear

## 5. View Results

Results are automatically committed to the repo:
- Latest: `output/stock_picks.csv`
- Historical: `output/stock_picks_YYYYMMDD.csv`

You can browse them directly on GitHub or pull them locally:

```bash
git pull
```

## 6. Customize Schedule (Optional)

Edit `.github/workflows/daily-scan.yml`:

```yaml
schedule:
  - cron: '0 21 * * 1-5'  # 9 PM UTC = 5 PM EST, Mon-Fri
```

Change the cron schedule if you want different timing:
- `0 22 * * 1-5` = 6 PM EST
- `0 14 * * *` = 10 AM EST (before market close)
- `30 20 * * 1-5` = 4:30 PM EST (right at market close)

## 7. Get Notifications (Optional)

Want email alerts when new picks are found?

1. Go to repo → Settings → Notifications
2. Enable "Actions" notifications
3. You'll get email if workflow fails

Or create a custom alert action (let me know if you want this).

## Troubleshooting

**Workflow fails?**
- Check "Actions" tab → click failed run → see error logs
- Common issue: permissions (should auto-fix)

**No output file generated?**
- Workflow may have run successfully but found no stocks
- Check if market was open (workflows skip weekends)

**Want to run locally?**
```bash
cd src
python main.py
```

Results save to `output/stock_picks.csv`