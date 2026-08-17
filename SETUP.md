# ZettaBrainSkill Setup Guide

Complete setup instructions to get ZettaBrainSkill running on your machine.

## Prerequisites

- Python 3.11 or higher
- pip or Poetry
- Docker Desktop (optional, for Ollama)
- 8GB+ RAM
- 10GB free disk space

## Step 1: Install Python (if needed)

### macOS
```bash
# Using Homebrew
brew install python@3.11
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### Windows
Download from https://www.python.org/downloads/

## Step 2: Install Ollama

Ollama provides easy local LLM inference.

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows
Download installer from https://ollama.com/download

## Step 3: Start Ollama and Pull Model

```bash
# Start Ollama server (keep this running in a terminal)
ollama serve

# In another terminal, pull Llama 3.1 8B model (~4.7GB download)
ollama pull llama3.1:8b

# Test it works
ollama run llama3.1:8b "Hello, tell me a joke"
```

**Note**: Keep `ollama serve` running whenever you use ZettaBrainSkill.

## Step 4: Install ZettaBrainSkill

### Option A: Using Poetry (Recommended)

```bash
# Navigate to project
cd zettabrainskill

# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Verify installation
zbs version
```

### Option B: Using pip

```bash
# Navigate to project
cd zettabrainskill

# Create virtual environment
python3.11 -m venv .venv

# Activate it
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Verify installation
zbs version
```

## Step 5: Verify Setup

```bash
# Check ZettaBrainSkill version
zbs version

# Check Ollama connection
zbs check
```

Expected output:
```
🔍 Checking Ollama status...
✓ Ollama is running and accessible

Model: llama3.1:8b
URL: http://localhost:11434
```

## Step 6: Run Your First Generation

```bash
# Validate the example skill
zbs validate examples/simple-summarizer.md

# Generate a summary
zbs generate examples/simple-summarizer.md \
  --input "Artificial intelligence is revolutionizing business operations. Companies leverage AI for customer service automation, predictive analytics, and process optimization. Key challenges include ensuring data quality, developing AI talent, and addressing ethical considerations around bias and privacy. Despite these hurdles, AI adoption continues to accelerate across all industries."
```

You should see a formatted summary with bullet points!

## Troubleshooting

### Error: "Ollama is not accessible"

**Solution**:
1. Make sure `ollama serve` is running
2. Check Ollama is on port 11434: `curl http://localhost:11434/api/tags`
3. Restart Ollama if needed

### Error: "Model not found"

**Solution**:
```bash
# List installed models
ollama list

# Pull the required model
ollama pull llama3.1:8b
```

### Error: "Poetry not found"

**Solution**:
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH (check Poetry installer output for exact command)
export PATH="$HOME/.local/bin:$PATH"
```

### Error: "Module not found"

**Solution**:
```bash
# Make sure you're in the virtual environment
poetry shell  # or source .venv/bin/activate

# Reinstall
poetry install  # or pip install -e .
```

### Slow Generation

**Solutions**:
- Use smaller model: `OLLAMA_MODEL=llama3.1:8b` (default)
- Reduce max_tokens: `--max-tokens 500`
- Check system resources (CPU/RAM usage)
- Consider using GPU if available

## Next Steps

### Create Your Own Skill

```bash
# Copy example
cp examples/simple-summarizer.md examples/my-skill.md

# Edit the skill
nano examples/my-skill.md

# Validate it
zbs validate examples/my-skill.md

# Use it
zbs generate examples/my-skill.md --input "Your text"
```

### Try Different Models

```bash
# Pull Mistral (smaller, faster)
ollama pull mistral:7b

# Use it (set environment variable)
OLLAMA_MODEL=mistral:7b zbs generate ...

# Or pull Qwen (good multilingual)
ollama pull qwen2.5:7b
```

### Adjust Generation Parameters

```bash
# More creative (higher temperature)
zbs generate skill.md --input "..." --temperature 0.9

# More deterministic (lower temperature)
zbs generate skill.md --input "..." --temperature 0.1

# Shorter output
zbs generate skill.md --input "..." --max-tokens 300

# Longer output
zbs generate skill.md --input "..." --max-tokens 3000
```

## Environment Configuration

Create `.env` file in project root:

```bash
# Copy example
cp .env.example .env

# Edit configuration
nano .env
```

Example `.env`:
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
SKILL_STORAGE_PATH=./data/skills
OUTPUT_STORAGE_PATH=./data/outputs
LOG_LEVEL=INFO
```

## Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=zettabrainskill

# Run specific test
poetry run pytest tests/unit/test_skill_parser.py

# Run with verbose output
poetry run pytest -v
```

## Development Setup

```bash
# Install dev dependencies
poetry install

# Format code
poetry run black zettabrainskill/

# Lint code
poetry run ruff check zettabrainskill/

# Type check
poetry run mypy zettabrainskill/
```

## System Requirements

### Minimum
- Python 3.11+
- 8GB RAM
- 10GB disk space
- CPU: 4 cores

### Recommended
- Python 3.11+
- 16GB RAM
- 50GB disk space (for multiple models)
- CPU: 8 cores or GPU (for faster inference)

### GPU Support (Optional)

For faster inference with larger models:

```bash
# Install CUDA (NVIDIA GPUs)
# Follow: https://developer.nvidia.com/cuda-downloads

# Pull larger model
ollama pull llama3.1:70b

# Ollama will automatically use GPU if available
```

## Getting Help

- **Documentation**: Check other .md files in project root
- **Examples**: See `examples/` directory
- **Issues**: [GitHub Issues - coming soon]
- **Email**: support@zettabrain.com

## Quick Reference

```bash
# Core commands
zbs version                    # Show version
zbs check                      # Check Ollama status
zbs validate <skill.md>        # Validate skill
zbs generate <skill.md> -i "..." # Generate document

# Common options
--input/-i        # Input text
--output/-o       # Output file
--temperature/-t  # Sampling temperature (0.0-2.0)
--max-tokens/-m   # Maximum output length
--business/-b     # Business ID

# Examples
zbs generate examples/simple-summarizer.md -i "text..." -o out.md
zbs generate examples/3rva-quote-simple.md -i "quote request" -t 0.2
```

---

**You're all set!** Start generating documents with AI 🚀

Try: `zbs generate examples/simple-summarizer.md --input "your text here"`
