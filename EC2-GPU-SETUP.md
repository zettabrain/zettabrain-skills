# EC2 GPU Instance Setup for 3RVA Demo

## Instance Recommendations

### GPU Instance Types (Fast)
- **g4dn.xlarge** - $0.526/hour - 4 vCPU, 16GB RAM, T4 GPU (Recommended)
- **g4dn.2xlarge** - $0.752/hour - 8 vCPU, 32GB RAM, T4 GPU (Faster)
- **g5.xlarge** - $1.006/hour - 4 vCPU, 16GB RAM, A10G GPU (Best)

### Region
- **US East (N. Virginia)** - us-east-1 (cheapest, closest)

---

## Step 1: Launch EC2 Instance

### AWS Console Setup

1. **Choose AMI**
   - Ubuntu Server 24.04 LTS
   - 64-bit (x86)

2. **Choose Instance Type**
   - g4dn.xlarge (or g4dn.2xlarge for faster)

3. **Configure Instance**
   - Auto-assign Public IP: **Enable**
   - Storage: 50GB gp3

4. **Security Group**
   - Add rules:
     - SSH: Port 22, Source: Your IP
     - HTTP: Port 80, Source: 0.0.0.0/0
     - Custom TCP: Port 8000, Source: 0.0.0.0/0

5. **Key Pair**
   - Create new or use existing
   - Download .pem file

---

## Step 2: Connect to Instance

```bash
# Set permissions on key
chmod 400 your-key.pem

# Connect
ssh -i your-key.pem ubuntu@YOUR_PUBLIC_IP
```

---

## Step 3: Install NVIDIA Drivers (GPU Instance)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install NVIDIA drivers
sudo apt install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# Reboot
sudo reboot

# Reconnect after reboot (wait 1 minute)
ssh -i your-key.pem ubuntu@YOUR_PUBLIC_IP

# Verify GPU
nvidia-smi
# Should show your T4 or A10G GPU
```

---

## Step 4: Install Ollama with GPU Support

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version

# Pull model (will use GPU automatically)
ollama pull llama3.1:8b

# Test
ollama run llama3.1:8b "Hello"
# Should respond quickly with GPU

# Check GPU usage
nvidia-smi
# Should show ollama using GPU memory
```

---

## Step 5: Install Python and Dependencies

```bash
# Install Python 3.12
sudo apt install -y python3.12 python3.12-venv python3-pip pipx

# Install system dependencies for WeasyPrint (PDF generation)
sudo apt install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libffi-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    libwebp-dev

# Ensure pipx is in PATH
pipx ensurepath
source ~/.bashrc
```

---

## Step 6: Install ZettaBrain Skills

```bash
# Install via pipx
pipx install git+https://github.com/zettabrain/zettabrain-skills.git

# Verify
zbs version
# Should show: ZettaBrainSkill version 0.4.0
```

---

## Step 7: Clone Repository

```bash
# Clone repo
cd ~
git clone https://github.com/zettabrain/zettabrain-skills.git
cd zettabrain-skills
```

---

## Step 8: Install Additional Dependencies

```bash
# Install PDF generation dependencies
pip install weasyprint markdown jinja2

# Or install from requirements
pip install -r requirements.txt 2>/dev/null || echo "No requirements.txt, continuing..."
```

---

## Step 9: Configure Environment

```bash
# Set generous timeout for complex quotes
echo 'export OLLAMA_TIMEOUT=900' >> ~/.bashrc
source ~/.bashrc

# Verify Ollama is accessible
curl http://localhost:11434/api/tags
```

---

## Step 10: Start Web Application

```bash
cd ~/zettabrain-skills
./start-web.sh
```

You should see:
```
🚀 Starting 3RVA Quote Generator Web App...

Access the app at:
  Local:    http://localhost:8000
  Network:  http://YOUR_PRIVATE_IP:8000

Press Ctrl+C to stop
```

---

## Step 11: Access from Your Phone/Tablet

### Get Your Public IP

In AWS Console:
1. Go to EC2 Dashboard
2. Select your instance
3. Copy **Public IPv4 address**

Example: `54.123.45.67`

### Access the App

On your phone/tablet browser:
```
http://54.123.45.67:8000
```

---

## Test the Application

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "ollama": "running",
  "version": "0.4.0"
}
```

### 2. Web Interface Test

Open browser: `http://YOUR_PUBLIC_IP:8000`

Should see:
- 🧊 3RVA Quote Generator
- Clean form interface

### 3. Generate Test Quote

1. Fill in customer request or use `?demo=1`
2. Click "Generate Quote"
3. Wait ~30 seconds (GPU is FAST!)
4. Verify you can download PDF

---

## Running in Background (Detached)

To keep app running after you disconnect:

```bash
# Install screen
sudo apt install -y screen

# Start in screen session
screen -S webapp

# Start app
cd ~/zettabrain-skills
./start-web.sh

# Detach: Press Ctrl+A, then D

# Reattach later
screen -r webapp

# List sessions
screen -ls
```

Or use systemd service:

```bash
# Create service file
sudo nano /etc/systemd/system/3rva-webapp.service
```

Paste:
```ini
[Unit]
Description=3RVA Quote Generator Web App
After=network.target ollama.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/zettabrain-skills
Environment="OLLAMA_TIMEOUT=900"
ExecStart=/home/ubuntu/.local/bin/uvicorn zettabrain_skills.web.app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable 3rva-webapp
sudo systemctl start 3rva-webapp

# Check status
sudo systemctl status 3rva-webapp

# View logs
sudo journalctl -u 3rva-webapp -f
```

---

## Performance with GPU

Expected generation times:
- **Simple quote (500 tokens)**: 10-20 seconds
- **Complex quote (1500 tokens)**: 30-60 seconds
- **vs CPU**: 5-10x faster with GPU!

---

## Security Considerations

### Production Security (Before Going Live)

1. **Restrict Port 8000**
   ```bash
   # Only allow your IP
   # In AWS Security Group:
   # Port 8000, Source: YOUR_IP/32
   ```

2. **Add HTTPS**
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   # Configure nginx as reverse proxy
   # Get SSL cert from Let's Encrypt
   ```

3. **Add Authentication**
   - Implement login system
   - Add API keys
   - Integrate with 3RVA's existing auth

4. **Use Private Subnets**
   - Place in VPC private subnet
   - Access via VPN or bastion host

### For Demo (Current Setup is OK)
- ✅ Public IP is fine
- ✅ Port 8000 open is fine
- ✅ No auth needed for demo
- ⚠️ Don't put real customer data yet

---

## Monitoring

### Check GPU Usage

```bash
# Watch GPU in real-time
watch -n 1 nvidia-smi

# Check Ollama
curl http://localhost:11434/api/ps
```

### Check System Resources

```bash
# CPU and memory
htop

# Disk space
df -h

# Network
sudo netstat -tulpn | grep 8000
```

---

## Troubleshooting

### GPU Not Detected

```bash
# Check driver
nvidia-smi

# Reinstall if needed
sudo apt install -y nvidia-driver-535
sudo reboot
```

### Ollama Not Using GPU

```bash
# Check Ollama status
systemctl status ollama

# View logs
sudo journalctl -u ollama -f

# Restart Ollama
sudo systemctl restart ollama
```

### Port 8000 Not Accessible

```bash
# Check if app is running
curl http://localhost:8000/health

# Check firewall
sudo ufw status

# Check AWS Security Group in console
# Ensure Port 8000 is open to 0.0.0.0/0
```

### PDF Generation Fails

```bash
# Install missing dependencies
sudo apt install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b

# Reinstall weasyprint
pip install --force-reinstall weasyprint
```

---

## Cost Optimization

### For Demo (Tonight)
- **g4dn.xlarge**: ~$0.50/hour
- **Run 2-3 hours**: ~$1.50
- **Stop instance after**: $0

### For Development
- Stop instance when not in use
- Use Spot Instances (60-70% cheaper)

### For Production
- Reserved Instances (1-year: 40% off)
- Or switch to CPU if GPU not needed

---

## After Demo

### Stop Instance (Save Money)

```bash
# From AWS Console
# Actions → Instance State → Stop

# Or via CLI
aws ec2 stop-instances --instance-ids i-XXXXXXXXX
```

### Terminate Instance (Delete)

```bash
# From AWS Console  
# Actions → Instance State → Terminate

# All data will be lost!
```

### Save AMI (Snapshot)

```bash
# From AWS Console
# Actions → Image and templates → Create image

# Name it: 3rva-demo-v1
# Can launch new instance from this later
```

---

## Quick Reference

### URLs
- Web App: `http://YOUR_PUBLIC_IP:8000`
- Demo: `http://YOUR_PUBLIC_IP:8000/?demo=1`
- Health: `http://YOUR_PUBLIC_IP:8000/health`

### Commands
```bash
# Start app
cd ~/zettabrain-skills && ./start-web.sh

# Check GPU
nvidia-smi

# Check Ollama
ollama list

# Check app
curl http://localhost:8000/health
```

---

## Success Checklist

Before demo:
- ✅ GPU detected (nvidia-smi shows GPU)
- ✅ Ollama installed and running
- ✅ Model downloaded (llama3.1:8b)
- ✅ Web app starts without errors
- ✅ Health check returns "healthy"
- ✅ Can access from phone: `http://PUBLIC_IP:8000`
- ✅ Demo URL works: `http://PUBLIC_IP:8000/?demo=1`
- ✅ Quote generates successfully
- ✅ PDF downloads work

---

Ready to impress Mike! 🚀
