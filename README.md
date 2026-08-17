# ZettaBrainSkill

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Open-source skill-based document generation platform with AI

Transform your business with AI-powered document automation using open-source models and portable skills.

## 🚀 Quick Install

### Ubuntu/Debian (Recommended)

```bash
# Install via pipx
pipx install git+https://github.com/zettabrain/zettabrainskill.git

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama and pull model
ollama serve &
ollama pull llama3.1:8b

# Verify
zbs version
zbs check
```

**📖 [Full Ubuntu Installation Guide](INSTALL-UBUNTU.md)**

### macOS

```bash
# Install Ollama
brew install ollama
ollama serve
ollama pull llama3.1:8b

# Install ZettaBrainSkill (development mode)
git clone https://github.com/zettabrain/zettabrainskill.git
cd zettabrainskill
poetry install
poetry shell
```

### From Source (Any OS)

```bash
# Clone repository
git clone https://github.com/zettabrain/zettabrainskill.git
cd zettabrainskill

# Install with Poetry
poetry install
poetry shell
```

### 3. Verify Installation

```bash
# Check version
zbs version

# Check Ollama connection
zbs check
```

### 4. Generate Your First Document

```bash
# Validate a skill
zbs validate examples/simple-summarizer.md

# Generate a summary
zbs generate examples/simple-summarizer.md \
  --input "Artificial intelligence is transforming businesses. Companies use AI for customer service, data analysis, and automation. Challenges include data quality and skilled personnel needs."

# Generate and save
zbs generate examples/simple-summarizer.md \
  --input "Your text here..." \
  --output summary.md
```

## Features

- 🎯 **Skill-Based**: Define tasks as portable skill files
- 🤖 **Open Source LLMs**: Use Llama, Mistral, Qwen locally
- 📚 **Business Agnostic**: Works for any industry
- 🏠 **Self-Hosted**: Full data control
- ⚡ **Fast**: Optimized for performance
- 🔧 **Extensible**: Add custom providers and skills

## Example Usage

### Summarize Text

```bash
zbs generate examples/simple-summarizer.md \
  --input "Your long text here..."
```

### Generate 3RVA Quote

```bash
zbs generate examples/3rva-quote-simple.md \
  --input "Customer needs 100 lbs R-22 delivered to Richmond, VA"
```

### Custom Parameters

```bash
zbs generate my-skill.md \
  --input "..." \
  --temperature 0.3 \
  --max-tokens 1000 \
  --output result.md
```

## Creating Skills

Skills are Markdown files with YAML frontmatter:

```markdown
---
name: my-skill
version: 1.0.0
description: What this skill does and when to use it
business_type: generic
temperature: 0.7
max_tokens: 2000
---

# Skill Instructions

Your instructions for the AI go here in Markdown format.

## Procedure

1. Step one
2. Step two
...
```

See `/examples` for more skill examples.

## CLI Commands

```bash
# Generate document
zbs generate <skill-file> --input "..." [--output file.md]

# Validate skill
zbs validate <skill-file>

# Check Ollama status
zbs check

# Show version
zbs version
```

## Project Structure

```
zettabrainskill/
├── zettabrainskill/          # Main package
│   ├── core/                 # Core models and engine
│   ├── skills/               # Skill parsing and management
│   ├── llm/                  # LLM providers
│   └── cli/                  # Command-line interface
├── examples/                 # Example skills
├── tests/                    # Test suite
└── docs/                     # Documentation
```

## Requirements

- Python 3.11+
- Ollama (for local LLM inference)
- 8GB+ RAM recommended

## Development

```bash
# Install dev dependencies
poetry install

# Run tests
poetry run pytest

# Format code
poetry run black zettabrainskill/

# Lint
poetry run ruff check zettabrainskill/
```

## Architecture

ZettaBrainSkill consists of:

1. **Skill Parser**: Parses YAML+Markdown skill files
2. **LLM Provider**: Abstraction layer for multiple LLM backends
3. **Generation Engine**: Orchestrates skill execution
4. **CLI**: User-friendly command-line interface

## Use Cases

- **Service Businesses**: Quotes, compliance responses, field documentation
- **Manufacturing**: RFQs, quality reports, equipment logs
- **Consulting**: Proposals, status reports, research memos
- **Healthcare**: Patient summaries, prior authorizations
- **And more**: Any repetitive document generation task

## Roadmap

- [x] Core skill parser and engine
- [x] Ollama provider
- [x] CLI interface
- [ ] REST API
- [ ] Vector database for corpus
- [ ] Citation system
- [ ] Discovery processor
- [ ] Web UI
- [ ] Additional LLM providers (vLLM, etc.)

## Documentation

- [Quick Start](../QUICK-START.md) - Detailed setup guide
- [Architecture](../ARCHITECTURE.md) - System design
- [Skill Specification](../SKILL-SPECIFICATION.md) - How to create skills
- [Implementation Roadmap](../IMPLEMENTATION-ROADMAP.md) - Development plan

## License

Apache 2.0

## Support

- GitHub Issues: [coming soon]
- Email: support@zettabrain.com
- Documentation: [coming soon]

## Acknowledgments

Built with inspiration from Claude Team Skills by Anthropic.

---

**Ready to automate your documents with AI?**

Start with `zbs check` to verify your setup, then try `zbs generate examples/simple-summarizer.md --input "your text"`
