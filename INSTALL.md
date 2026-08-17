# ZettaBrain Skills - Installation Guide

Complete installation instructions for Ubuntu 24.04 (EC2 or local).

## Quick Start (EC2 GPU Instance)

### 1. Launch EC2 Instance

**Recommended:** g4dn.xlarge (GPU for fast generation)
- Ubuntu 24.04 LTS
- 30GB storage minimum
- Security group: Allow inbound TCP port 8000 (for web access)

### 2. Connect to Instance

```bash
ssh -i your-key.pem ubuntu@<ec2-public-ip>
```

### 3. Install System Dependencies

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install system libraries for WeasyPrint (PDF generation)
sudo apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    git \
    python3-pip
```

### 4. Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve &

# Wait a few seconds, then pull the model (this takes ~5 minutes)
ollama pull llama3.1:8b
```

**Verify Ollama:**
```bash
curl http://localhost:11434/api/tags
# Should return list of installed models
```

### 5. Clone Repository

```bash
cd ~
git clone https://github.com/zettabrain/zettabrain-skills.git
cd zettabrain-skills
```

### 6. Install Python Dependencies

```bash
pip install fastapi uvicorn python-multipart weasyprint markdown jinja2 \
    httpx pyyaml python-frontmatter rich pydantic starlette anyio click \
    --break-system-packages --ignore-installed typing-extensions
```

**Note:** `--break-system-packages` is required for Ubuntu 24.04's externally-managed Python.

### 7. Set Environment Variables (Optional)

```bash
# Increase timeout for large documents
export OLLAMA_TIMEOUT=300

# Use different model (optional)
export OLLAMA_MODEL=llama3.1:8b
```

### 8. Start Web Application

```bash
./start-web.sh
```

**Output:**
```
✓ Loaded business context for 3RVA
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 9. Access Web Application

**From your laptop:**
```
http://<ec2-public-ip>:8000
```

**From your phone/tablet:**
- Connect to same network or use public IP
- Open browser
- Go to: `http://<ec2-public-ip>:8000`

## Verification

### Test Ollama
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Hello",
  "stream": false
}'
```

### Test Web App Health
```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "ollama": "running",
  "business_context_loaded": true,
  "business_name": "3RVA",
  "version": "0.5.0"
}
```

### Access Web Interface
Open browser to `http://<ec2-public-ip>:8000`
- You should see the ZettaBrain Skills home page
- Multiple industry skills should be displayed
- Business context banner should show "3RVA"

## Troubleshooting

### Port 8000 Not Accessible

**Check EC2 Security Group:**
1. Go to EC2 Console
2. Select your instance
3. Click "Security" tab
4. Edit inbound rules
5. Add rule: Type=Custom TCP, Port=8000, Source=0.0.0.0/0

**Check if app is running:**
```bash
ps aux | grep uvicorn
```

**Check logs:**
```bash
# If running in background
tail -f nohup.out
```

### Ollama Not Running

```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
ollama serve &

# Verify
curl http://localhost:11434/api/tags
```

### Model Not Found

```bash
# List installed models
ollama list

# Pull model if missing
ollama pull llama3.1:8b
```

### WeasyPrint Errors

```bash
# Reinstall system dependencies
sudo apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info
```

### Python Import Errors

```bash
# Reinstall all dependencies
pip install fastapi uvicorn python-multipart weasyprint markdown jinja2 \
    httpx pyyaml python-frontmatter rich pydantic starlette anyio click \
    --break-system-packages --ignore-installed typing-extensions --force-reinstall
```

### Discovery Document Not Loading

```bash
# Check if file exists
ls -la examples/discovery-documents/3rva-discovery.md

# Check startup logs for errors
# Look for: "✓ Loaded business context for 3RVA"
```

## Running in Background

### Option 1: Using nohup
```bash
nohup ./start-web.sh > app.log 2>&1 &
```

**View logs:**
```bash
tail -f app.log
```

**Stop:**
```bash
pkill -f uvicorn
```

### Option 2: Using screen
```bash
# Start screen session
screen -S zettabrain

# Start app
./start-web.sh

# Detach: Ctrl+A then D

# Reattach later
screen -r zettabrain
```

### Option 3: Using systemd (Production)

Create service file:
```bash
sudo nano /etc/systemd/system/zettabrain-skills.service
```

Content:
```ini
[Unit]
Description=ZettaBrain Skills Web Application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/zettabrain-skills
ExecStart=/usr/bin/python3 -m uvicorn zettabrain_skills.web.app:app --host 0.0.0.0 --port 8000
Restart=always
Environment="OLLAMA_TIMEOUT=300"
Environment="OLLAMA_MODEL=llama3.1:8b"

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable zettabrain-skills
sudo systemctl start zettabrain-skills

# Check status
sudo systemctl status zettabrain-skills

# View logs
sudo journalctl -u zettabrain-skills -f
```

## Performance Optimization

### GPU Instance (Recommended)
- **g4dn.xlarge** - Best balance of cost/performance
- Generation time: 30-60 seconds
- Cost: ~$0.50/hour

### CPU Instance (Budget)
- **t3.large** or larger
- Generation time: 2-5 minutes
- Cost: ~$0.08/hour

### Increase Ollama Timeout
```bash
export OLLAMA_TIMEOUT=600
```

## Updates

### Pull Latest Changes
```bash
cd ~/zettabrain-skills
git pull origin main

# Restart web app
pkill -f uvicorn
./start-web.sh
```

### Update Dependencies
```bash
pip install --upgrade fastapi uvicorn python-multipart weasyprint markdown \
    jinja2 httpx pyyaml python-frontmatter rich pydantic starlette anyio click \
    --break-system-packages
```

## Configuration

### Change Port
Edit `start-web.sh`:
```bash
uvicorn zettabrain_skills.web.app:app --host 0.0.0.0 --port 9000
```

### Change Model
```bash
export OLLAMA_MODEL=llama3.1:70b
```

### Add Custom Discovery Document
```bash
# Add your business discovery document
nano examples/discovery-documents/my-business-discovery.md

# Update app.py to load it
nano zettabrain_skills/web/app.py
# Change: discovery_path = Path("examples/discovery-documents/my-business-discovery.md")
```

## Security Notes

### For Production:
1. **Use HTTPS:** Set up nginx reverse proxy with SSL
2. **Restrict Access:** Update security group to specific IPs
3. **Authentication:** Add user authentication (future feature)
4. **Firewall:** Use UFW to restrict ports
5. **Updates:** Keep system and packages updated

### Basic Firewall Setup
```bash
sudo ufw allow 22    # SSH
sudo ufw allow 8000  # Web app
sudo ufw enable
```

## CLI Usage (Optional)

The CLI is also available:

```bash
# Check Ollama status
zbs check

# Validate a skill
zbs validate examples/3rva-quote-full.md

# Generate document
zbs generate examples/3rva-quote-full.md \
    --input "Need 100 lbs R-410A" \
    --output quote.txt

# Parse discovery document
zbs discovery parse examples/discovery-documents/3rva-discovery.md
```

## Next Steps

1. **Generate Test Document**
   - Go to `http://<ec2-public-ip>:8000`
   - Select "3RVA Quote Full"
   - Enter sample request
   - Generate and download PDF

2. **View Business Info**
   - Go to `/discovery`
   - Verify 3RVA information loaded

3. **Try Other Industries**
   - Generate legal contract review
   - Generate restaurant menu description
   - Show multi-industry capability

4. **Demo to Mike**
   - Use phone to access web app
   - Show real-time quote generation
   - Download professional PDF
   - Demonstrate platform capability

## Support

**Issues?**
- Check `/health` endpoint: `http://<ec2-public-ip>:8000/health`
- View logs: `tail -f app.log` or `sudo journalctl -u zettabrain-skills -f`
- GitHub Issues: https://github.com/zettabrain/zettabrain-skills/issues

**Common Questions:**
- Generation takes 2+ minutes? Use GPU instance or increase timeout
- Can't access from phone? Check security group port 8000
- Discovery document not loading? Check file exists and restart app
- PDF generation fails? Reinstall WeasyPrint system dependencies
