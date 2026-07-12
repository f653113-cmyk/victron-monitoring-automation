# Victron Solar Monitoring Automation

Fully automated solar monitoring system that fetches data from Victron VRM, analyzes performance, detects anomalies, and sends beautiful reports via email.

## Features

✅ **Automated Data Fetching** - Daily sync from Victron VRM API  
✅ **KPI Calculations** - Production, efficiency, battery health, load analysis  
✅ **Anomaly Detection** - Automatic issue identification  
✅ **Beautiful Dashboards** - Tableau/Power BI level HTML visualizations  
✅ **Email Reports** - Weekly alerts (if issues) + monthly comprehensive reports  
✅ **GitHub Native** - Runs on GitHub Actions, no server needed  
✅ **Zero Manual Work** - Fully automated after setup  

## Setup Instructions

### Step 1: Prepare Your GitHub Repository

1. Go to your GitHub repo: `f653113/victron-monitoring-automation`
2. Create these folders:
   - `.github/workflows/`
   - `data/`
   - `reports/`

### Step 2: Add Files to GitHub

Upload these files to your repo:

**Root directory:**
- `victron_fetcher.py`
- `analyzer.py`
- `dashboard_generator.py`
- `email_sender.py`
- `requirements.txt`
- `README.md`

**.github/workflows/ directory:**
- `daily_sync.yml`
- `weekly_check.yml`
- `monthly_report.yml`

### Step 3: Configure GitHub Secrets

Go to your GitHub repo Settings → Secrets and Variables → Actions

Add these secrets:

1. **VICTRON_API_TOKEN**
   - Value: `d9fa84df-85b3-490a-99be-ee8db64492ac`

2. **GMAIL_ADDRESS**
   - Value: `f653113@gmail.com`

3. **GMAIL_PASSWORD**
   - Value: `vxrpvlvzqhtiojmj` (your Gmail App Password)

4. **EMAIL_RECIPIENTS**
   - Value: `gkipkirui@givepower.org` (or multiple emails comma-separated)

### Step 4: Enable GitHub Actions

1. Go to repo Settings → Actions
2. Click "Allow all actions and reusable workflows"
3. Click "Save"

### Step 5: Test the System

1. Go to Actions tab
2. Select "Daily Data Sync"
3. Click "Run workflow"
4. Wait for it to complete
5. Check your email for the report

## Automation Schedule

**Daily (00:00 UTC)**
- Fetches latest data from Victron
- Runs analysis
- Generates dashboard
- Stores data in GitHub

**Weekly (Monday 08:00 UTC)**
- Checks for anomalies
- IF issues found: Sends alert email
- IF no issues: Skips email

**Monthly (1st @ 09:00 UTC)**
- Generates comprehensive report
- ALWAYS sends email with full analysis
- Saves reports to GitHub

## File Structure

```
victron-monitoring-automation/
├── .github/workflows/
│   ├── daily_sync.yml          # Daily data fetch
│   ├── weekly_check.yml        # Weekly anomaly check
│   └── monthly_report.yml      # Monthly comprehensive report
├── data/                       # Data storage
│   ├── raw/                    # Raw Victron API data
│   └── processed/              # Processed analysis
├── reports/                    # Generated reports
│   └── dashboard.html          # Interactive dashboard
├── victron_fetcher.py          # Data fetcher
├── analyzer.py                 # Data analysis
├── dashboard_generator.py      # Visualization generator
├── email_sender.py             # Email delivery
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Monitoring Metrics

The system tracks:

- **Production** - Total kWh produced per site
- **Efficiency** - System efficiency percentage
- **Battery SOC** - State of charge (avg, min, max)
- **Load** - Inverter load percentage
- **Peak Power** - Maximum power output
- **Anomalies** - Issues requiring attention

## Email Reports

### Weekly Alert (if anomalies)
- Summary of issues detected
- Site-by-site breakdown
- Recommended actions

### Monthly Comprehensive Report
- Executive summary with KPIs
- Performance by site
- Efficiency trends
- Anomaly log
- Dashboard HTML attachment

## Troubleshooting

**Emails not arriving:**
- Check GMAIL_PASSWORD is the App Password (not main password)
- Verify EMAIL_RECIPIENTS format (email@domain.com)
- Check GitHub Actions logs for errors

**Data not updating:**
- Verify VICTRON_API_TOKEN is correct
- Check Actions tab for workflow errors
- Manually trigger workflow to test

**Workflow fails:**
- Go to Actions tab
- Click the failed workflow
- Check "Run workflow" logs for errors

## Support

For issues or feature requests, create an issue in the GitHub repo.

## License

Private use for GivePower

---

**Last Updated:** July 2026  
**Version:** 1.0.0
