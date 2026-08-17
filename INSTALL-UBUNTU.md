# Installing ZettaBrain Skills on Ubuntu

Complete installation guide for Ubuntu 20.04, 22.04, and 24.04.

## Quick Install (Recommended)

```bash
# Install via pipx (isolated environment)
pipx install git+https://github.com/zettabrain/zettabrain-skills.git

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama and pull model
ollama serve &
ollama pull llama3.1:8b

# Verify installation
zbs version
zbs check
```

## Detailed Installation

### Step 1: System Requirements

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Check Python version (need 3.11+)
python3 --version
```

If Python < 3.11, install it:

```bash
# Add deadsnakes PPA (for Ubuntu 20.04/22.04)
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# Verify
python3.11 --version
```

### Step 2: Install pipx (Recommended Method)

```bash
# Install pipx
sudo apt install pipx -y

# Ensure pipx is in PATH
pipx ensurepath

# Restart shell or run
source ~/.bashrc

# Verify
pipx --version
```

### Step 3: Install ZettaBrain Skills

#### Option A: Install from GitHub (pipx)

```bash
# Install latest version
pipx install git+https://github.com/zettabrain/zettabrain-skills.git

# Or install specific version/branch
pipx install git+https://github.com/zettabrain/zettabrain-skills.git@main

# Verify installation
zbs version
```

#### Option B: Install from GitHub (pip)

```bash
# Install globally (not recommended)
pip install git+https://github.com/zettabrain/zettabrain-skills.git

# Or in a virtual environment (recommended)
python3.11 -m venv zbs-env
source zbs-env/bin/activate
pip install git+https://github.com/zettabrain/zettabrain-skills.git

# Verify
zbs version
```

#### Option C: Install from Source (Development)

```bash
# Clone repository
git clone https://github.com/zettabrain/zettabrain-skills.git
cd zettabrain-skills

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Install dependencies and ZettaBrain Skills
poetry install

# Activate environment
poetry shell

# Verify
zbs version
```

### Step 4: Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

### Step 5: Setup Ollama

#### Start Ollama as a Service

```bash
# Ollama installs as systemd service automatically
# Check status
systemctl status ollama

# If not running, start it
sudo systemctl start ollama

# Enable on boot
sudo systemctl enable ollama
```

#### Pull Models

```bash
# Pull Llama 3.1 8B (recommended, ~4.7GB)
ollama pull llama3.1:8b

# Or smaller/faster options:
ollama pull mistral:7b           # ~4.1GB
ollama pull qwen2.5:7b          # ~4.4GB

# Or larger/better quality:
ollama pull llama3.1:70b        # ~40GB, needs GPU
```

### Step 6: Verify Installation

```bash
# Check ZettaBrain Skills version
zbs version

# Check Ollama connection
zbs check

# Expected output:
# ✓ Ollama is running and accessible
# Model: llama3.1:8b
# URL: http://localhost:11434
```

### Step 7: Test with Example

```bash
# Create a test skill
cat > test-skill.md << 'EOF'
---
name: hello-world
version: 1.0.0
description: A simple test skill
---

# Hello World Skill

Generate a friendly greeting based on the user's input.

## Instructions
1. Read the user's name from the input
2. Generate a warm, friendly greeting
3. Keep it under 2 sentences
EOF

# Validate skill
zbs validate test-skill.md

# Generate greeting
zbs generate test-skill.md --input "My name is Alex"

# You should see a friendly greeting!
```

## Installation Methods Comparison

| Method | Pros | Cons | Use Case |
|--------|------|------|----------|
| **pipx** | Isolated, clean, easy updates | Requires pipx | Production, end users |
| **pip (venv)** | Standard Python workflow | Manual venv management | Development |
| **Poetry** | Best for development | More complex setup | Contributors |
| **pip (global)** | Simple | Can conflict with system | Not recommended |

## Troubleshooting

### Issue: "zbs: command not found" after pipx install

**Solution**:
```bash
# Ensure pipx path is in PATH
pipx ensurepath

# Restart shell
exec $SHELL

# Or manually add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: "Ollama is not accessible"

**Solutions**:
```bash
# Check if Ollama service is running
systemctl status ollama

# If not running
sudo systemctl start ollama

# Check logs if issues
journalctl -u ollama -f

# Test manually
curl http://localhost:11434/api/tags
```

### Issue: Python 3.11 not available

**Solution**:
```bash
# For Ubuntu 20.04/22.04, use deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv -y

# For Ubuntu 24.04, Python 3.11+ is default
sudo apt install python3 python3-venv -y
```

### Issue: "Model not found"

**Solution**:
```bash
# List installed models
ollama list

# Pull the required model
ollama pull llama3.1:8b

# Verify it's available
ollama list | grep llama
```

### Issue: Slow generation

**Solutions**:
```bash
# Use smaller model
ollama pull mistral:7b
export OLLAMA_MODEL=mistral:7b

# Reduce max tokens
zbs generate skill.md --input "..." --max-tokens 500

# Check system resources
htop  # or top

# Consider GPU acceleration (if you have NVIDIA GPU)
# Install CUDA toolkit: https://developer.nvidia.com/cuda-downloads
```

## Updating ZettaBrain Skills

### Update via pipx

```bash
# Update to latest version
pipx upgrade zettabrain-skills

# Or reinstall
pipx uninstall zettabrain-skills
pipx install git+https://github.com/zettabrain/zettabrain-skills.git
```

### Update via pip

```bash
# If using venv
source zbs-env/bin/activate
pip install --upgrade git+https://github.com/zettabrain/zettabrain-skills.git
```

### Update from source

```bash
cd zettabrain-skills
git pull
poetry install
```

## Uninstalling

### Remove via pipx

```bash
pipx uninstall zettabrain-skills
```

### Remove via pip

```bash
pip uninstall zettabrain-skills
```

### Remove Ollama

```bash
# Stop service
sudo systemctl stop ollama
sudo systemctl disable ollama

# Remove Ollama
sudo rm -rf /usr/local/bin/ollama
sudo rm -rf /usr/share/ollama
sudo rm -rf ~/.ollama

# Remove systemd service
sudo rm /etc/systemd/system/ollama.service
sudo systemctl daemon-reload
```

## Advanced Configuration

### Set Custom Ollama URL

```bash
# Set environment variable
export OLLAMA_BASE_URL=http://your-server:11434

# Or create config file
mkdir -p ~/.config/zettabrain-skills
cat > ~/.config/zettabrain-skills/config.yaml << EOF
ollama:
  base_url: http://your-server:11434
  model: llama3.1:8b
EOF
```

### Run Ollama on Different Port

```bash
# Edit systemd service
sudo systemctl edit ollama

# Add:
[Service]
Environment="OLLAMA_HOST=0.0.0.0:8080"

# Restart
sudo systemctl restart ollama

# Update ZettaBrain Skills config
export OLLAMA_BASE_URL=http://localhost:8080
```

### Use GPU Acceleration

```bash
# Install NVIDIA drivers
ubuntu-drivers devices
sudo ubuntu-drivers autoinstall

# Install CUDA (if not already installed)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update
sudo apt install cuda -y

# Verify GPU is available
nvidia-smi

# Ollama will automatically use GPU
# Pull a larger model to leverage GPU
ollama pull llama3.1:70b
```

## System Service Setup (Optional)

Run ZettaBrain Skills as a service for API mode (future feature):

```bash
# Create service file
sudo tee /etc/systemd/system/zettabrain-skills.service << EOF
[Unit]
Description=ZettaBrain Skills API Server
After=network.target ollama.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME
ExecStart=/home/$USER/.local/bin/zbs serve
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable zettabrain-skills
sudo systemctl start zettabrain-skills
```

## Quick Reference

```bash
# Installation
pipx install git+https://github.com/zettabrain/zettabrain-skills.git

# Update
pipx upgrade zettabrain-skills

# Commands
zbs version                           # Show version
zbs check                             # Check Ollama status
zbs validate skill.md                 # Validate skill
zbs generate skill.md -i "text"       # Generate document
zbs generate skill.md -i "..." -o out.md  # Save to file

# Ollama
ollama list                           # List models
ollama pull llama3.1:8b              # Pull model
ollama rm llama3.1:8b                # Remove model
systemctl status ollama               # Check service status
```

## Getting Help

- **Documentation**: https://github.com/zettabrain/zettabrain-skills
- **Issues**: https://github.com/zettabrain/zettabrain-skills/issues
- **Email**: support@zettabrain.com

## Next Steps

1. Create your first skill: See `examples/` directory
2. Read the docs: Check out SKILL-SPECIFICATION.md
3. Join the community: [Discord - coming soon]

---

**Installation complete!** 🎉

Try it now: `zbs generate examples/simple-summarizer.md --input "your text here"`
