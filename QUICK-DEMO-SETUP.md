# Quick Demo Setup - Tonight's Presentation

## On Your Ubuntu Server (5 Minutes)

### Step 1: Update ZettaBrain Skills

```bash
# Upgrade to latest version with web app
pipx upgrade zettabrain-skills

# Or reinstall
pipx uninstall zettabrain-skills
pipx install git+https://github.com/zettabrain/zettabrain-skills.git
```

### Step 2: Get Latest Files

```bash
cd ~
git clone https://github.com/zettabrain/zettabrain-skills.git
cd zettabrain-skills
```

### Step 3: Install Jinja2

```bash
pip install jinja2
```

### Step 4: Start Web App

```bash
cd ~/zettabrain-skills
./start-web.sh
```

You'll see:
```
🚀 Starting 3RVA Quote Generator Web App...

Access the app at:
  Local:    http://localhost:8000
  Network:  http://10.0.1.185:8000

Press Ctrl+C to stop
```

### Step 5: Open Firewall (If Needed)

```bash
sudo ufw allow 8000
```

### Step 6: Get Your Server IP

```bash
hostname -I | awk '{print $1}'
```

Example output: `10.0.1.185`

---

## Access the App

### From Your Phone

1. Make sure phone is on same WiFi network as server
2. Open browser (Safari, Chrome, etc.)
3. Go to: `http://10.0.1.185:8000` (use your server IP)

### From Your Laptop

1. Same network as server
2. Open browser
3. Go to: `http://10.0.1.185:8000`

---

## Demo Flow (2 Minutes)

### 1. Open App
Visit `http://YOUR_IP:8000`

### 2. Try Pre-Filled Demo
Add `?demo=1` to URL: `http://YOUR_IP:8000/?demo=1`

### 3. Generate Quote
Click "Generate Quote" button

### 4. Wait ~2 Minutes
Shows loading spinner

### 5. Show Mike
- Professional quote with pricing
- Copy/print/download buttons
- Past quotes list

---

## If Something Goes Wrong

### Web App Won't Start

```bash
# Check if Ollama is running
ollama list

# Start Ollama if needed
sudo systemctl start ollama

# Check if port 8000 is available
sudo lsof -i :8000

# Use different port if needed
python3 -m uvicorn zettabrain_skills.web.app:app --host 0.0.0.0 --port 8080
```

### Can't Access from Phone

```bash
# Check server IP again
hostname -I

# Make sure firewall allows connections
sudo ufw allow 8000
sudo ufw status

# Test from server itself first
curl http://localhost:8000/health
```

### Generation Timeout

```bash
# Stop app (Ctrl+C)

# Set longer timeout
export OLLAMA_TIMEOUT=1200

# Restart
./start-web.sh
```

---

## Alternative: Manual Customer Request

If demo data doesn't work, manually paste:

```
Emergency request from Premier HVAC Services. Medical office building AC is down in Glen Allen VA. Need 100 lbs R-22 reclaimed refrigerant delivered same-day to 4500 Cox Road, Glen Allen VA 23060. Critical - patients on site. Need by 4pm today. Contact John Martinez at (804) 555-1234.
```

Fill in:
- **Customer Name:** Premier HVAC Services
- **Email:** john@premierhvac.com
- **Phone:** (804) 555-1234
- **Request:** [paste above]

---

## What Mike Will See

1. **Simple form** - paste customer request
2. **One button** - "Generate Quote"
3. **Professional quote** - full pricing, delivery, tax
4. **Easy actions** - copy, print, download
5. **Quote history** - see all past quotes

---

## Key Points for Mike

✅ "Paste customer email or notes here"
✅ "Click generate - takes 2 minutes"
✅ "Professional quote ready to send"
✅ "Copy and paste into your email"
✅ "Works on your phone anywhere"
✅ "All quotes saved automatically"

---

## After Demo

If Mike loves it:

1. Collect his feedback
2. Ask about CRM integration
3. Discuss email automation
4. Plan Phase 2 features

---

## Backup Plan

If web app has issues during demo:

**Fall back to CLI:**
```bash
zbs generate examples/3rva-quote-full.md \
  --input "Customer needs 100 lbs R-22..." \
  --output demo-quote.md

cat demo-quote.md
```

Still impressive, just not as pretty!

---

## Contact Info

After demo, get:
- Mike's email for follow-up
- His CRM system (if any)
- His current quote process
- Pain points he wants solved
- Budget/timeline for Phase 2

---

Good luck! 🍀
