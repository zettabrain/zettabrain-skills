# Install ZettaBrain Skills on Ubuntu 24.04 (Noble)

Ubuntu 24.04 comes with Python 3.12 by default - perfect for ZettaBrain Skills!

## Complete Installation (5 minutes)

### Step 1: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Python 3.12 and pip

```bash
# Install Python dependencies
sudo apt install -y python3.12 python3.12-venv python3-pip pipx

# Ensure pipx is in PATH
pipx ensurepath
source ~/.bashrc
```

### Step 3: Install ZettaBrain Skills

```bash
# Install via pipx
pipx install git+https://github.com/zettabrain/zettabrain-skills.git

# Verify installation
zbs version
```

### Step 4: Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service (runs automatically as systemd service)
sudo systemctl start ollama
sudo systemctl enable ollama

# Pull Llama 3.1 model
ollama pull llama3.1:8b

# Verify Ollama is working
ollama list
```

### Step 5: Verify Everything Works

```bash
# Check ZettaBrain Skills
zbs version

# Check Ollama connection
zbs check

# Test generation
zbs generate examples/simple-summarizer.md \
  --input "Artificial intelligence is revolutionizing business operations and enabling new capabilities in automation and decision-making"
```

## One-Command Installation

Copy and paste this entire block:

```bash
sudo apt update && \
sudo apt install -y python3.12 python3.12-venv python3-pip pipx && \
pipx ensurepath && \
source ~/.bashrc && \
pipx install git+https://github.com/zettabrain/zettabrain-skills.git && \
curl -fsSL https://ollama.com/install.sh | sh && \
sudo systemctl start ollama && \
sudo systemctl enable ollama && \
ollama pull llama3.1:8b && \
zbs version && \
zbs check
```

## Expected Output

After installation:

```bash
$ zbs version
ZettaBrain Skills version 0.1.0

$ zbs check
🔍 Checking Ollama status...
✓ Ollama is running and accessible

Model: llama3.1:8b
URL: http://localhost:11434
```

## Quick Start Examples

### 1. Summarize Text

```bash
zbs generate examples/simple-summarizer.md \
  --input "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience. It focuses on developing algorithms that can access data and use it to learn patterns."
```

### 2. Generate Service Quote

```bash
zbs generate examples/3rva-quote-simple.md \
  --input "Customer needs 100 lbs R-22 refrigerant delivered to Richmond, VA by Friday"
```

### 3. Save Output to File

```bash
zbs generate examples/simple-summarizer.md \
  --input "Your long text here..." \
  --output summary.md

cat summary.md
```

### 4. Adjust Parameters

```bash
# More deterministic (factual)
zbs generate skill.md --input "text" --temperature 0.2

# Shorter output
zbs generate skill.md --input "text" --max-tokens 300
```

## Troubleshooting

### pipx not found after install

```bash
# Reload shell
source ~/.bashrc

# Or logout and login again
exit
# Then login again
```

### zbs command not found

```bash
# Check if pipx installed it
pipx list

# Ensure PATH is set
pipx ensurepath
source ~/.bashrc

# Manually add to PATH if needed
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Ollama not running

```bash
# Check status
sudo systemctl status ollama

# Start if not running
sudo systemctl start ollama

# Check with zbs
zbs check
```

### Model not found

```bash
# List installed models
ollama list

# Pull the model
ollama pull llama3.1:8b

# Try smaller/faster models
ollama pull mistral:7b
```

## Additional Models

```bash
# Smaller, faster (4GB)
ollama pull mistral:7b

# Larger, better quality (40GB, needs GPU)
ollama pull llama3.1:70b

# Good multilingual support
ollama pull qwen2.5:7b
```

## Useful Aliases

Add to `~/.bashrc`:

```bash
# Quick shortcuts
alias zbsv='zbs version'
alias zbsc='zbs check'
alias zbsg='zbs generate'

# Quick summarize function
summarize() {
  zbs generate examples/simple-summarizer.md --input "$1"
}
```

Then:
```bash
source ~/.bashrc

# Use aliases
zbsc
summarize "Your text here"
```

## Upgrading

```bash
# Upgrade to latest version
pipx upgrade zettabrain-skills

# Or reinstall
pipx uninstall zettabrain-skills
pipx install git+https://github.com/zettabrain/zettabrain-skills.git
```

## Uninstalling

```bash
# Remove ZettaBrain Skills
pipx uninstall zettabrain-skills

# Remove Ollama
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm -rf /usr/local/bin/ollama
sudo rm -rf /usr/share/ollama
sudo rm -rf ~/.ollama

# Remove systemd service
sudo rm /etc/systemd/system/ollama.service
sudo systemctl daemon-reload
```

## System Requirements

### Minimum
- Ubuntu 24.04 (Noble)
- 2 CPU cores
- 8GB RAM
- 20GB disk space

### Recommended
- 4+ CPU cores
- 16GB RAM
- 50GB disk space (for multiple models)

### With GPU (Optional)
- NVIDIA GPU with 8GB+ VRAM
- CUDA toolkit installed
- Enables much faster generation with larger models

## Creating Your Own Skills

See the skill specification:
- [Skill Specification](https://github.com/zettabrain/zettabrain-skills/blob/main/SKILL-SPECIFICATION.md)
- [Examples Directory](https://github.com/zettabrain/zettabrain-skills/tree/main/examples)

## Getting Help

- **Issues**: https://github.com/zettabrain/zettabrain-skills/issues
- **Documentation**: https://github.com/zettabrain/zettabrain-skills
- **Quick Reference**: https://github.com/zettabrain/zettabrain-skills/blob/main/QUICKREF.md

## Success!

You should now have:
- ✅ ZettaBrain Skills installed
- ✅ Ollama running with Llama 3.1
- ✅ `zbs` command available
- ✅ Example skills ready to use

Test it:
```bash
zbs generate examples/simple-summarizer.md \
  --input "Artificial intelligence is transforming industries worldwide"
```

Enjoy! 🚀
