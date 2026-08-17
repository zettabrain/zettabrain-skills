#!/bin/bash

# ZettaBrainSkill Publishing Script (using GitHub CLI)
# This script uses 'gh' CLI to create and publish the repository

set -e  # Exit on error

echo "🚀 ZettaBrainSkill Publishing Script (GitHub CLI)"
echo "=================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Not in zettabrain-skills directory"
    exit 1
fi

echo "✓ In correct directory"
echo ""

# Check if gh is authenticated
echo "🔐 Checking GitHub authentication..."
if ! gh auth status > /dev/null 2>&1; then
    echo "❌ Not authenticated with GitHub CLI"
    echo "Please run: gh auth login"
    exit 1
fi

echo "✓ Authenticated with GitHub"
echo ""

# Show current status
echo "📋 Current git status:"
git status --short
echo ""

# Ask for confirmation
read -p "Do you want to commit all changes and publish? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

# Stage all files
echo "📦 Staging all files..."
git add .
echo "✓ Files staged"
echo ""

# Create commit (check if there are changes)
if git diff --cached --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Creating commit..."
    git commit -m "Initial release: ZettaBrainSkill v0.1.0

Core features:
- Skill parser and validator (YAML + Markdown)
- LLM provider abstraction (Ollama)
- Document generation engine
- CLI interface (zbs command)
- Example skills (summarizer, quotes)
- Comprehensive documentation
- Ubuntu installation via pipx/pip
- Unit tests with pytest

Installation:
  pipx install git+https://github.com/zettabrain/zettabrain-skills.git

Ready for production use."

    echo "✓ Commit created"
fi

echo ""
echo "🏗️  Creating GitHub repository..."
echo ""

# Create repository using gh
if gh repo create zettabrain/zettabrain-skills \
    --public \
    --source=. \
    --remote=origin \
    --description="Open-source skill-based document generation platform with AI" \
    --push; then

    echo ""
    echo "✅ Repository created and code pushed!"
    echo ""
    echo "📝 Repository: https://github.com/zettabrain/zettabrain-skills"
    echo ""

    # Add topics
    echo "🏷️  Adding repository topics..."
    gh repo edit zettabrain/zettabrain-skills \
        --add-topic=ai \
        --add-topic=llm \
        --add-topic=document-generation \
        --add-topic=python \
        --add-topic=ollama \
        --add-topic=automation \
        --add-topic=nlp \
        --add-topic=skills

    echo "✓ Topics added"
    echo ""

    # Create release
    echo "🎁 Creating release v0.1.0..."
    gh release create v0.1.0 \
        --title "ZettaBrainSkill v0.1.0 - Initial Release" \
        --notes "# ZettaBrainSkill v0.1.0 🎉

First public release of ZettaBrainSkill - open-source skill-based document generation platform.

## Installation

### Ubuntu/Debian
\`\`\`bash
pipx install git+https://github.com/zettabrain/zettabrain-skills.git
\`\`\`

See [INSTALL-UBUNTU.md](https://github.com/zettabrain/zettabrain-skills/blob/main/INSTALL-UBUNTU.md) for detailed instructions.

### From Source
\`\`\`bash
git clone https://github.com/zettabrain/zettabrain-skills.git
cd zettabrain-skills
poetry install
poetry shell
\`\`\`

## Features

✅ Skill parser and validator (YAML + Markdown)
✅ LLM provider abstraction (Ollama)
✅ Document generation engine
✅ CLI interface (\`zbs\` command)
✅ Example skills (summarizer, quotes)
✅ Comprehensive documentation
✅ Unit tests

## Quick Start

\`\`\`bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull llama3.1:8b

# Verify installation
zbs version
zbs check

# Generate your first document
zbs generate examples/simple-summarizer.md --input \"your text here\"
\`\`\`

## Documentation

- [Installation Guide (Ubuntu)](https://github.com/zettabrain/zettabrain-skills/blob/main/INSTALL-UBUNTU.md)
- [Setup Guide](https://github.com/zettabrain/zettabrain-skills/blob/main/SETUP.md)
- [Quick Reference](https://github.com/zettabrain/zettabrain-skills/blob/main/QUICKREF.md)
- [README](https://github.com/zettabrain/zettabrain-skills/blob/main/README.md)

## What's Next

See our roadmap for upcoming features:
- Vector database integration (Qdrant)
- REST API
- Discovery processor
- Web UI

## Links

- 📖 [Documentation](https://github.com/zettabrain/zettabrain-skills)
- 🐛 [Report Issues](https://github.com/zettabrain/zettabrain-skills/issues)
- 💬 [Discussions](https://github.com/zettabrain/zettabrain-skills/discussions)"

    echo "✓ Release created"
    echo ""

    echo "🎉 SUCCESS! ZettaBrainSkill is now published!"
    echo ""
    echo "📍 Repository: https://github.com/zettabrain/zettabrain-skills"
    echo "📦 Release: https://github.com/zettabrain/zettabrain-skills/releases/tag/v0.1.0"
    echo ""
    echo "🧪 Test installation:"
    echo "  pipx install git+https://github.com/zettabrain/zettabrain-skills.git"
    echo ""
    echo "📊 Next steps:"
    echo "  - View repository: gh repo view zettabrain/zettabrain-skills --web"
    echo "  - Enable Discussions: Settings → Features → Discussions"
    echo "  - Add collaborators: Settings → Collaborators"
    echo ""

else
    echo ""
    echo "❌ Failed to create repository"
    echo ""
    echo "This might be because:"
    echo "1. Repository already exists - Check: https://github.com/zettabrain/zettabrain-skills"
    echo "2. No permission to create in 'zettabrain' org"
    echo "3. Network issue"
    echo ""
    echo "If repository exists, you can push manually:"
    echo "  git remote add origin https://github.com/zettabrain/zettabrain-skills.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
    exit 1
fi
