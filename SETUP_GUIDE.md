# Complete Setup Guide

Follow these steps to deploy the automated monitoring system.

---

## Step 1: Add Files to GitHub Repository

### Files to Add:

**In root directory:**
1. `victron_fetcher.py`
2. `analyzer.py`
3. `dashboard_generator.py`
4. `email_sender.py`
5. `requirements.txt`
6. `README.md`

**In `.github/workflows/` directory:**
1. `daily_sync.yml`
2. `weekly_check.yml`
3. `monthly_report.yml`

### How to Add Files:

**Option A: Upload via GitHub Web Interface (Easiest)**

1. Go to: https://github.com/f653113/victron-monitoring-automation
2. Click "Add file" → "Upload files"
3. Drag and drop the Python files
4. Click "Commit changes"
5. Repeat for each file

**Option B: Create Files via GitHub Web Interface**

1. Click "Add file" → "Create new file"
2. Name: `victron_fetcher.py`
3. Paste the code content
4. Click "Commit new file"
5. Repeat for each file

---

## Step 2: Create Folders

GitHub automatically creates folders, but you can pre-create:

1. Click "Add file" → "Create new file"
2. Name: `.github/workflows/daily_sync.yml`
3. Paste workflow content
4. Commit

Repeat for other workflow files.

---

## Step 3: Configure GitHub Secrets

### Go to Settings:
1. GitHub repo → Settings (top menu)
2. Left sidebar: "Secrets and variables" → "Actions"

### Add Secret 1: VICTRON_API_TOKEN
1. Click "New repository secret"
2. **Name:** `VICTRON_API_TOKEN`
3. **Value:** `d9fa84df-85b3-490a-99be-ee8db64492ac`
4. Click "Add secret"

### Add Secret 2: GMAIL_ADDRESS
1. Click "New repository secret"
2. **Name:** `GMAIL_ADDRESS`
3. **Value:** `f653113@gmail.com`
4. Click "Add secret"

### Add Secret 3: GMAIL_PASSWORD
1. Click "New repository secret"
2. **Name:** `GMAIL_PASSWORD`
3. **Value:** `vxrpvlvzqhtiojmj`
4. Click "Add secret"

### Add Secret 4: EMAIL_RECIPIENTS
1. Click "New repository secret"
2. **Name:** `EMAIL_RECIPIENTS`
3. **Value:** `gkipkirui@givepower.org`
   - For multiple recipients: `email1@domain.com,email2@domain.com`
4. Click "Add secret"

---

## Step 4: Enable GitHub Actions

1. GitHub repo → Settings (top menu)
2. Left sidebar: "Actions" → "General"
3. Under "Actions permissions":
   - Select: "Allow all actions and reusable workflows"
4. Click "Save"

---

## Step 5: Test the System

### Manual Test:

1. GitHub repo → "Actions" tab
2. Left sidebar: "Daily Data Sync"
3. Click "Run workflow"
4. Select branch: `main`
5. Click "Run workflow"
6. Wait 2-3 minutes for completion

### Check Results:

1. After workflow completes, check:
   - **Email:** Should receive data in `gkipkirui@givepower.org`
   - **GitHub:** Check "data/" and "reports/" folders for new files

### If Email Not Received:

1. Go to Actions tab
2. Click the failed workflow run
3. Check logs for errors
4. Common issues:
   - Gmail App Password incorrect
   - Recipient email format wrong
   - Network/SMTP error

---

## Step 6: Set Up Automation Schedule

The workflows run automatically on schedule:

**Daily (00:00 UTC):**
- Data fetches automatically

**Weekly (Monday 08:00 UTC):**
- Checks for anomalies
- Sends email if issues found

**Monthly (1st @ 09:00 UTC):**
- Generates full report
- Always sends email

---

## Step 7: Customize (Optional)

### Change Email Recipients:

1. Settings → Secrets → `EMAIL_RECIPIENTS`
2. Update value: `new.email@domain.com`
3. Save

### Change Schedule Times:

1. Edit `.github/workflows/daily_sync.yml`
2. Find: `- cron: '0 0 * * *'`
3. Change to desired time (UTC)
   - `'0 9 * * *'` = 9 AM UTC daily
   - `'0 8 * * 1'` = 8 AM UTC Mondays

### Add More Recipients:

1. Update `EMAIL_RECIPIENTS` secret:
   - `email1@domain.com,email2@domain.com,email3@domain.com`

---

## Verification Checklist

- [ ] All 6 Python files uploaded
- [ ] All 3 workflow files in `.github/workflows/`
- [ ] VICTRON_API_TOKEN secret added
- [ ] GMAIL_ADDRESS secret added
- [ ] GMAIL_PASSWORD secret added
- [ ] EMAIL_RECIPIENTS secret added
- [ ] GitHub Actions enabled
- [ ] Manual test completed successfully
- [ ] Email received at recipient address
- [ ] Dashboard HTML generated in `reports/`

---

## Next Steps

1. **Review First Report**
   - Check email for dashboard
   - Review data quality
   - Provide feedback to Claude

2. **Iterate Until Perfect**
   - Adjust visualizations
   - Change metrics/thresholds
   - Fine-tune scheduling

3. **Go Live**
   - System runs automatically
   - No manual input needed
   - Reports arrive weekly/monthly

---

## Support

**Workflow Not Running?**
- Check Actions tab for error messages
- Verify secrets are set correctly
- Manually trigger to test

**Email Not Sending?**
- Verify Gmail password is App Password
- Check recipient email format
- Review email_sender.py logs

**Data Not Fetching?**
- Verify Victron API token
- Check internet connectivity
- Review victron_fetcher.py logs

---

**You're all set! The system is now fully automated and will run on schedule.** 🚀
