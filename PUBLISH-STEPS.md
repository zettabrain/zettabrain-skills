# Quick Publishing Steps

Execute these commands to publish ZettaBrain Skills to GitHub.

## Prerequisites Checklist

- [ ] Have access to https://github.com/zettabrain organization
- [ ] Git configured with your credentials
- [ ] All code reviewed and tested

## Step-by-Step Commands

### 1. Navigate to Project

```bash
cd /Users/olajideshobowale/Documents/ZettaBrain/Business/3rva/zettabrain-skills
```

### 2. Create GitHub Repository

Go to: https://github.com/organizations/zettabrain/repositories/new

- **Name**: `zettabrain-skills`
- **Description**: `Open-source skill-based document generation platform with AI`
- **Public**: ✓
- **Do NOT initialize** (we have code)

Click "Create repository"

### 3. Verify Git Setup

```bash
# Check git status
git status

# If not initialized
git init

# Configure user
git config user.name "Your Name"
git config user.email "your@email.com"
```

### 4. Add and Commit All Files

```bash
# Add all files
git add .

# Review what will be committed
git status

# Create initial commit
git commit -m "Initial release: ZettaBrain Skills v0.1.0

Core features:
- Skill parser and validator
- LLM provider abstraction (Ollama)
- Document generation engine
- CLI interface (zbs command)
- Example skills
- Comprehensive documentation
- Unit tests
"
```

### 5. Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/zettabrain/zettabrain-skills.git

# Verify remote
git remote -v

# Rename branch to main (if needed)
git branch -M main

# Push
git push -u origin main
```

### 6. Create Release on GitHub

Go to: https://github.com/zettabrain/zettabrain-skills/releases/new

- **Tag**: `v0.1.0`
- **Title**: `ZettaBrain Skills v0.1.0 - Initial Release`
- **Description**: Copy from template below

```markdown
# ZettaBrain Skills v0.1.0 🎉

First public release of ZettaBrain Skills - open-source skill-based document generation platform.

## Installation

Ubuntu/Debian:
\`\`\`bash
pipx install git+https://github.com/zettabrain/zettabrain-skills.git
\`\`\`

See [INSTALL-UBUNTU.md](INSTALL-UBUNTU.md) for details.

## Features

✅ Skill parser and validator
✅ LLM provider abstraction (Ollama)
✅ Document generation engine
✅ CLI interface
✅ Example skills
✅ Full documentation

## Quick Start

\`\`\`bash
ollama pull llama3.1:8b
zbs check
zbs generate examples/simple-summarizer.md --input "your text"
\`\`\`

## Links

- [Documentation](README.md)
- [Installation Guide](INSTALL-UBUNTU.md)
- [Quick Reference](QUICKREF.md)
```

Click "Publish release"

### 7. Configure Repository

On GitHub Settings page:

**Topics**: Add these tags
- ai
- llm
- document-generation
- python
- ollama
- automation
- nlp
- skills

**Features**: Enable
- ✓ Issues
- ✓ Discussions
- ✓ Wikis

### 8. Test Installation

```bash
# In a new terminal/machine
pipx install git+https://github.com/zettabrain/zettabrain-skills.git

# Verify
zbs version
zbs check
```

## Verification Checklist

After publishing, verify:

- [ ] Repository visible at https://github.com/zettabrain/zettabrain-skills
- [ ] README displays correctly with badges
- [ ] Installation via pipx works
- [ ] Examples folder is visible
- [ ] License file is present
- [ ] Issues are enabled
- [ ] Release v0.1.0 is published
- [ ] Topics/tags are set

## Troubleshooting

### Remote Already Exists

```bash
git remote remove origin
git remote add origin https://github.com/zettabrain/zettabrain-skills.git
```

### Permission Denied

Use HTTPS instead of SSH:
```bash
git remote set-url origin https://github.com/zettabrain/zettabrain-skills.git
```

### Unrelated Histories

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## Post-Publishing

1. **Announce** on social media (optional)
2. **Monitor** Issues tab for bug reports
3. **Update** documentation as needed
4. **Create** project board for feature tracking

## Quick Command Summary

```bash
# Setup and push
cd /Users/olajideshobowale/Documents/ZettaBrain/Business/3rva/zettabrain-skills
git add .
git commit -m "Initial release: ZettaBrain Skills v0.1.0"
git remote add origin https://github.com/zettabrain/zettabrain-skills.git
git branch -M main
git push -u origin main

# Test installation
pipx install git+https://github.com/zettabrain/zettabrain-skills.git
zbs version
```

---

**Ready to publish!** 🚀

Follow steps 1-8 above to complete the publication.
