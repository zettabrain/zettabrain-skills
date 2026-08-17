# ZettaBrainSkill Quick Reference

One-page reference for common tasks.

## Installation

```bash
# Ubuntu/Debian (pipx - recommended)
pipx install git+https://github.com/zettabrain/zettabrainskill.git

# Ubuntu/Debian (pip with venv)
python3 -m venv zbs-env && source zbs-env/bin/activate
pip install git+https://github.com/zettabrain/zettabrainskill.git

# From source (any OS)
git clone https://github.com/zettabrain/zettabrainskill.git
cd zettabrainskill && poetry install && poetry shell
```

## Ollama Setup

```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh  # Linux
brew install ollama                              # macOS

# Start server
ollama serve

# Pull models
ollama pull llama3.1:8b          # Recommended (4.7GB)
ollama pull mistral:7b           # Faster (4.1GB)
ollama pull llama3.1:70b         # Better quality (40GB, GPU)
```

## CLI Commands

```bash
# Check installation
zbs version                      # Show version
zbs check                        # Check Ollama status

# Validate skill
zbs validate skill.md            # Check skill is valid

# Generate document
zbs generate skill.md --input "text"
zbs generate skill.md -i "text" -o output.md
zbs generate skill.md -i "text" -t 0.3 -m 500

# Options
-i, --input TEXT        Input text (required)
-o, --output PATH       Output file path
-t, --temperature FLOAT Temperature (0.0-2.0)
-m, --max-tokens INT    Max output length
-b, --business TEXT     Business ID
```

## Skill File Format

```markdown
---
name: my-skill
version: 1.0.0
description: What this does and when to use it
business_type: generic
temperature: 0.7
max_tokens: 2000
tags: [category, type]
---

# Skill Instructions

Your instructions for the AI in Markdown.

## Procedure
1. Step one
2. Step two

## Output Format
\`\`\`
Expected output format
\`\`\`

## Never
- Don't do X
- Don't do Y
```

## Common Skill Templates

### Summarizer
```yaml
name: summarizer
temperature: 0.5
max_tokens: 500
```

### Quote Generator
```yaml
name: quote-gen
temperature: 0.2
max_tokens: 1500
requires_discovery: [pricing-rules]
```

### Report Writer
```yaml
name: report-writer
temperature: 0.7
max_tokens: 3000
citation_required: true
```

## Environment Variables

```bash
# Ollama configuration
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3.1:8b

# Storage paths
export SKILL_STORAGE_PATH=./data/skills
export OUTPUT_STORAGE_PATH=./data/outputs
```

## Ollama Management

```bash
# List models
ollama list

# Remove model
ollama rm llama3.1:8b

# Check service
systemctl status ollama          # Linux
ps aux | grep ollama             # macOS

# View logs
journalctl -u ollama -f          # Linux systemd
```

## Troubleshooting

```bash
# "zbs: command not found"
pipx ensurepath && exec $SHELL
export PATH="$HOME/.local/bin:$PATH"

# "Ollama not accessible"
ollama serve &                   # Start server
curl http://localhost:11434/api/tags  # Test connection

# "Model not found"
ollama list                      # Check installed
ollama pull llama3.1:8b         # Install model

# Slow generation
ollama pull mistral:7b          # Use smaller model
zbs generate skill.md -i "..." -m 500  # Reduce tokens
```

## Development

```bash
# Run tests
poetry run pytest
poetry run pytest -v            # Verbose
poetry run pytest --cov         # With coverage

# Code quality
poetry run black zettabrainskill/
poetry run ruff check zettabrainskill/
poetry run mypy zettabrainskill/

# Update dependencies
poetry update
```

## Example Usage

```bash
# Summarize text
zbs generate examples/simple-summarizer.md \
  --input "Long text to summarize here..." \
  --output summary.md

# Generate quote
zbs generate examples/3rva-quote-simple.md \
  --input "Customer needs 100 lbs R-22 in Richmond" \
  --temperature 0.2

# Custom skill
cat > my-skill.md << 'EOF'
---
name: email-writer
version: 1.0.0
description: Write professional emails
temperature: 0.7
---
# Email Writer
Write a professional email based on the user's request.
Be concise and polite.
EOF

zbs generate my-skill.md \
  --input "Write email to client about project delay"
```

## File Locations

```
~/.local/bin/zbs                 # CLI binary (pipx)
~/.local/pipx/venvs/zettabrainskill/  # pipx venv
~/.ollama/                       # Ollama data
/usr/local/bin/ollama           # Ollama binary
~/.config/zettabrainskill/      # Config (future)
```

## Python API (Future)

```python
from zettabrainskill.skills.parser import load_skill
from zettabrainskill.core.engine import GenerationEngine
from zettabrainskill.core.models import GenerationRequest

# Load skill
skill = load_skill("my-skill.md")

# Create engine
engine = GenerationEngine()

# Generate
request = GenerationRequest(input="Hello world")
result = engine.generate(skill, request)

print(result.content)
```

## Links

- **Repo**: https://github.com/zettabrain/zettabrainskill
- **Issues**: https://github.com/zettabrain/zettabrainskill/issues
- **Install Guide**: [INSTALL-UBUNTU.md](INSTALL-UBUNTU.md)
- **Setup Guide**: [SETUP.md](SETUP.md)
- **Ollama**: https://ollama.com

## Getting Help

```bash
# Built-in help
zbs --help
zbs generate --help

# Check status
zbs check

# Validate your skill
zbs validate my-skill.md
```

---

**Quick start**: `pipx install git+https://github.com/zettabrain/zettabrainskill.git && ollama pull llama3.1:8b && zbs check`
