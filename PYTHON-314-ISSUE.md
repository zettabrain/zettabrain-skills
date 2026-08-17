# Python 3.14 Compatibility Issue

## Problem

Python 3.14 is very new (released 2026) and some dependencies aren't fully compatible yet.

**Error**:
```
TypeError: TyperArgument.make_metavar() takes 1 positional argument but 2 were given
```

This happens even with the latest typer (0.12.5) because Python 3.14 introduced breaking changes.

## Solution: Use Python 3.11 or 3.12

### Option 1: Install with Python 3.12 (Recommended)

```bash
# 1. Install Python 3.12
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev -y

# 2. Uninstall current version
pipx uninstall zettabrain-skills

# 3. Install pipx with Python 3.12
python3.12 -m pip install --user pipx
python3.12 -m pipx ensurepath

# 4. Restart shell
exec $SHELL

# 5. Install zettabrain-skills using Python 3.12
pipx install --python python3.12 git+https://github.com/zettabrain/zettabrain-skills.git

# 6. Verify
zbs version
python3.12 --version
```

### Option 2: Install with Python 3.11

```bash
# 1. Install Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# 2. Uninstall current version
pipx uninstall zettabrain-skills

# 3. Install pipx with Python 3.11
python3.11 -m pip install --user pipx
python3.11 -m pipx ensurepath

# 4. Restart shell
exec $SHELL

# 5. Install zettabrain-skills using Python 3.11
pipx install --python python3.11 git+https://github.com/zettabrain/zettabrain-skills.git

# 6. Verify
zbs version
python3.11 --version
```

### Option 3: Use venv with Python 3.11/3.12

```bash
# Create venv with Python 3.12
python3.12 -m venv ~/.zbs-env

# Activate it
source ~/.zbs-env/bin/activate

# Install zettabrain-skills
pip install git+https://github.com/zettabrain/zettabrain-skills.git

# Test
zbs version

# Add to .bashrc for convenience
echo 'alias zbs="~/.zbs-env/bin/zbs"' >> ~/.bashrc
source ~/.bashrc
```

## Quick Fix Command

For Python 3.12:

```bash
sudo apt update && \
sudo apt install -y python3.12 python3.12-venv python3.12-dev && \
pipx uninstall zettabrain-skills && \
python3.12 -m pip install --user pipx && \
python3.12 -m pipx ensurepath && \
exec $SHELL && \
pipx install --python python3.12 git+https://github.com/zettabrain/zettabrain-skills.git
```

## Verify Working Installation

After installing with Python 3.11 or 3.12:

```bash
# Check Python version used by zbs
pipx runpip zettabrain-skills show zettabrain-skills | grep Location

# Should show python3.11 or python3.12 in the path, NOT python3.14

# Test it works
zbs version
zbs check

# This should now work (with quotes!)
zbs generate examples/simple-summarizer.md \
  --input "Artificial intelligence is transforming business operations"
```

## Why This Happens

- **Python 3.14** is very new (released 2026)
- **typer/click** haven't been updated for Python 3.14 breaking changes yet
- **Python 3.11/3.12** are stable and well-supported
- This is a temporary issue until libraries catch up

## System Python Version

Check what Python versions you have:

```bash
# List all Python versions
ls -la /usr/bin/python*

# Check default
python3 --version

# You probably have:
python3.14 --version  # Too new!
python3.12 --version  # Good ✓
python3.11 --version  # Good ✓
```

## Alternative: Docker (If Available)

If you have Docker, use Python 3.12 container:

```bash
docker run -it python:3.12-slim bash

# Inside container:
pip install git+https://github.com/zettabrain/zettabrain-skills.git
zbs version
```

## Checking Your Installation

```bash
# What Python version is pipx using?
pipx list --verbose

# Should show:
# zettabrain-skills 0.1.0
#   package zettabrain-skills 0.1.0, installed using Python 3.12.x
#   - zbs
#   - zettabrain-skills
```

## Expected Output After Fix

```bash
$ zbs version
ZettaBrain Skills version 0.1.0

$ zbs generate examples/simple-summarizer.md --input "Test"
📖 Loading skill from examples/simple-summarizer.md...
✓ Loaded skill: simple-summarizer v1.0.0
🚀 Initializing generation engine...
✓ Connected to Ollama (llama3.1:8b)
⚙️  Generating document...

[Generated content appears here]
```

## Future Support

When typer/click are updated for Python 3.14 compatibility, this issue will be resolved automatically. For now, use Python 3.11 or 3.12.

## Need Help?

If still having issues:

1. Check Python version: `python3 --version`
2. Check pipx Python: `pipx list --verbose`
3. Open issue: https://github.com/zettabrain/zettabrain-skills/issues

Include:
- Python version
- Ubuntu version: `lsb_release -a`
- pipx version: `pipx --version`
- Error message
