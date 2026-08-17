# Install Python 3.12 on Ubuntu

## Method 1: Add Deadsnakes PPA (Recommended)

```bash
# Add the deadsnakes PPA (repository for newer Python versions)
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Now install Python 3.12
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Verify installation
python3.12 --version
```

## Method 2: Use Python 3.11 (Might Already Be Installed)

Check if Python 3.11 is available:

```bash
# Check what Python versions you have
python3.11 --version

# If it works, use Python 3.11 instead:
pipx uninstall zettabrain-skills
pipx install --python python3.11 git+https://github.com/zettabrain/zettabrain-skills.git
```

## Method 3: Use System Python with venv

If you can't install Python 3.12, use a virtual environment:

```bash
# Check your Python version
python3 --version

# If it's 3.14, we need to downgrade or use venv differently
# Create venv with whatever Python you have
python3 -m venv ~/.zbs-env

# Activate it
source ~/.zbs-env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install with specific package versions that might work better
pip install git+https://github.com/zettabrain/zettabrain-skills.git

# Test
zbs version
```

## Complete Installation Steps

### Step 1: Add Deadsnakes PPA
```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
```

### Step 2: Install Python 3.12
```bash
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3.12-distutils
```

### Step 3: Install pip for Python 3.12
```bash
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
```

### Step 4: Install pipx with Python 3.12
```bash
python3.12 -m pip install --user pipx
python3.12 -m pipx ensurepath
source ~/.bashrc
```

### Step 5: Install zettabrain-skills
```bash
pipx uninstall zettabrain-skills
pipx install --python python3.12 git+https://github.com/zettabrain/zettabrain-skills.git
```

### Step 6: Verify
```bash
zbs version
pipx list --verbose | grep python
```

## Quick One-Liner

```bash
sudo apt update && \
sudo apt install -y software-properties-common && \
sudo add-apt-repository ppa:deadsnakes/ppa -y && \
sudo apt update && \
sudo apt install -y python3.12 python3.12-venv python3.12-dev && \
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12 && \
python3.12 -m pip install --user pipx && \
python3.12 -m pipx ensurepath && \
source ~/.bashrc && \
pipx uninstall zettabrain-skills && \
pipx install --python python3.12 git+https://github.com/zettabrain/zettabrain-skills.git
```

## Troubleshooting

### Can't add PPA?
If `add-apt-repository` doesn't work:

```bash
# Manually add the PPA
sudo sh -c 'echo "deb http://ppa.launchpad.net/deadsnakes/ppa/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/deadsnakes-ppa.list'
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F23C5A6CF475977595C89F51BA6932366A755776
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev
```

### Still can't install?
Check your Ubuntu version:

```bash
lsb_release -a
```

- Ubuntu 22.04 (Jammy): ✓ Supports Python 3.12 via deadsnakes
- Ubuntu 20.04 (Focal): ✓ Supports Python 3.12 via deadsnakes  
- Ubuntu 18.04 (Bionic): ⚠️  May have issues

## Alternative: Use Docker

If all else fails, use Docker:

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Run with Python 3.12
docker run -it --rm python:3.12-slim bash

# Inside container:
pip install git+https://github.com/zettabrain/zettabrain-skills.git
zbs version
```

## Check What You Have

```bash
# List all Python versions installed
ls -la /usr/bin/python*

# Check each version
python3 --version
python3.11 --version
python3.12 --version
python3.14 --version
```
