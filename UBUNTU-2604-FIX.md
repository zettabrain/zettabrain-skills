# Ubuntu 26.04 (Resolute) - Python 3.12 Installation

## Your Situation

You're on **Ubuntu 26.04 (resolute)** which comes with Python 3.14 by default. Python 3.12 might not be available yet from deadsnakes for this very new Ubuntu release.

## Solution 1: Check Available Python Versions

```bash
# See what Python versions deadsnakes provides for your system
apt-cache search python3. | grep deadsnakes

# Or list all available python packages
apt list python3.* | grep deadsnakes
```

## Solution 2: Try Python 3.11

Python 3.11 should work and might be available:

```bash
# Try installing Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# If that works:
python3.11 --version

# Install zettabrain-skills with Python 3.11
pipx uninstall zettabrain-skills
python3.11 -m pip install --user pipx
python3.11 -m pipx ensurepath
source ~/.bashrc
pipx install --python python3.11 git+https://github.com/zettabrain/zettabrain-skills.git
```

## Solution 3: Build Python 3.12 from Source

If no compatible Python is available, build from source:

```bash
# Install build dependencies
sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev \
  libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev \
  libsqlite3-dev wget libbz2-dev

# Download Python 3.12
cd /tmp
wget https://www.python.org/ftp/python/3.12.8/Python-3.12.8.tgz
tar -xf Python-3.12.8.tgz
cd Python-3.12.8

# Configure and build (takes 5-10 minutes)
./configure --enable-optimizations --prefix=/usr/local
make -j$(nproc)
sudo make altinstall

# Verify
/usr/local/bin/python3.12 --version

# Install zettabrain-skills
pipx uninstall zettabrain-skills
/usr/local/bin/python3.12 -m pip install --user pipx
/usr/local/bin/python3.12 -m pipx ensurepath
source ~/.bashrc
pipx install --python /usr/local/bin/python3.12 git+https://github.com/zettabrain/zettabrain-skills.git
```

## Solution 4: Use Docker (Easiest)

The fastest solution is Docker with Python 3.12:

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Pull Python 3.12 image
docker pull python:3.12-slim

# Run zettabrain-skills in Docker
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  python:3.12-slim bash

# Inside the container:
pip install git+https://github.com/zettabrain/zettabrain-skills.git
zbs version

# Install Ollama separately on host, then use it from container
# by exposing host network:
docker run -it --rm --network host python:3.12-slim bash
pip install git+https://github.com/zettabrain/zettabrain-skills.git
zbs generate examples/simple-summarizer.md --input "test"
```

## Solution 5: Use Conda/Miniconda

Install Miniconda and create Python 3.12 environment:

```bash
# Install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
echo 'export PATH="$HOME/miniconda/bin:$PATH"' >> ~/.bashrc

# Create Python 3.12 environment
conda create -n zbs python=3.12 -y
conda activate zbs

# Install zettabrain-skills
pip install git+https://github.com/zettabrain/zettabrain-skills.git

# Use it
zbs version

# Add alias for convenience
echo 'alias zbs="$HOME/miniconda/envs/zbs/bin/zbs"' >> ~/.bashrc
```

## Quick Decision Tree

```
Can you install Python 3.11 from apt?
├─ YES → Use Python 3.11
└─ NO
   ├─ Have Docker?
   │  └─ YES → Use Docker (easiest)
   └─ NO
      ├─ Want quick solution?
      │  └─ Use Conda/Miniconda
      └─ Want system install?
         └─ Build Python 3.12 from source
```

## Recommended: Docker Method

This is the quickest and cleanest:

```bash
# One-time setup
curl -fsSL https://get.docker.com | sh

# Create a helper script
cat > ~/zbs-docker.sh << 'EOF'
#!/bin/bash
docker run -it --rm --network host \
  -v $(pwd):/workspace \
  -w /workspace \
  python:3.12-slim \
  bash -c "pip install -q git+https://github.com/zettabrain/zettabrain-skills.git && zbs $@"
EOF

chmod +x ~/zbs-docker.sh

# Use it
~/zbs-docker.sh version
~/zbs-docker.sh check
~/zbs-docker.sh generate examples/simple-summarizer.md --input "test"

# Add alias
echo 'alias zbs="~/zbs-docker.sh"' >> ~/.bashrc
source ~/.bashrc

# Now use normally
zbs version
```

## What to Try First

Run this to see what's available:

```bash
# Check available Python versions
apt-cache search "^python3\.[0-9]+-dev" | grep -E "3\.(11|12|13)"

# If you see python3.11-dev or python3.12-dev, install that version
# If not, use Docker (easiest) or build from source
```

## Why This Happens

- Ubuntu 26.04 (resolute) is brand new
- Ships with Python 3.14
- Python 3.14 is too new for typer/click
- Deadsnakes PPA may not have older versions for resolute yet
- Need to use Python 3.11 or 3.12

## Expected After Fix

```bash
$ zbs version
ZettaBrain Skills version 0.1.0

$ zbs generate examples/simple-summarizer.md --input "AI test"
# Works! ✓
```
