# Publishing ZettaBrain Skills to GitHub

Step-by-step guide to publish the repository to https://github.com/zettabrain

## Prerequisites

- GitHub account with access to `zettabrain` organization
- Git installed locally
- Repository prepared (already done ✓)

## Step 1: Create GitHub Repository

### Via GitHub Web Interface

1. Go to https://github.com/organizations/zettabrain/repositories/new
2. Fill in details:
   - **Repository name**: `zettabrain-skills`
   - **Description**: `Open-source skill-based document generation platform with AI`
   - **Visibility**: Public ✓
   - **Initialize repository**: ❌ Do NOT check (we have code already)
3. Click "Create repository"

### Via GitHub CLI (Alternative)

```bash
# If you have gh CLI installed
gh repo create zettabrain/zettabrain-skills \
  --public \
  --description "Open-source skill-based document generation platform with AI" \
  --source=. \
  --remote=origin
```

## Step 2: Prepare Local Repository

```bash
# Navigate to project
cd /Users/olajideshobowale/Documents/ZettaBrain/Business/3rva/zettabrain-skills

# Check git status (should be initialized)
git status

# Configure git user (if not already done)
git config user.name "Your Name"
git config user.email "your-email@example.com"
```

## Step 3: Stage and Commit Files

```bash
# Add all files
git add .

# Check what will be committed
git status

# Create initial commit
git commit -m "Initial commit: ZettaBrain Skills v0.1.0

- Core skill parser and validator
- LLM provider abstraction (Ollama)
- Document generation engine
- CLI interface (zbs command)
- Example skills (summarizer, 3RVA quotes)
- Comprehensive documentation
- Unit tests

Features:
- Skill-based document generation
- Open-source LLM support (Llama, Mistral, Qwen)
- Business-agnostic platform
- Self-hosted, full data control
- Fast local inference with Ollama
"
```

## Step 4: Add Remote and Push

```bash
# Add GitHub remote
git remote add origin https://github.com/zettabrain/zettabrain-skills.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main

# If main branch doesn't exist, create it
git branch -M main
git push -u origin main
```

## Step 5: Configure Repository Settings

### On GitHub Web Interface

1. Go to https://github.com/zettabrain/zettabrain-skills

2. **Settings → General**
   - Features: ✓ Wikis, ✓ Issues, ✓ Projects
   - Pull Requests: ✓ Allow merge commits

3. **Settings → Branches**
   - Add branch protection rule for `main`:
     - ✓ Require pull request reviews before merging
     - ✓ Require status checks to pass (after CI setup)

4. **Settings → Topics**
   - Add topics: `ai`, `llm`, `document-generation`, `python`, `ollama`, `automation`, `skills`, `nlp`

## Step 6: Create Release

### Via GitHub Web Interface

1. Go to https://github.com/zettabrain/zettabrain-skills/releases/new
2. Fill in:
   - **Tag version**: `v0.1.0`
   - **Release title**: `ZettaBrain Skills v0.1.0 - Initial Release`
   - **Description**:
     ```markdown
     # ZettaBrain Skills v0.1.0 - Initial Release 🎉
     
     First public release of ZettaBrain Skills - an open-source skill-based document generation platform.
     
     ## Features
     
     - ✅ Skill parser and validator (YAML + Markdown)
     - ✅ LLM provider abstraction (Ollama support)
     - ✅ Document generation engine
     - ✅ CLI interface (`zbs` command)
     - ✅ Example skills (text summarization, service quotes)
     - ✅ Comprehensive documentation
     - ✅ Unit tests
     
     ## Installation
     
     ### Ubuntu/Debian
     ```bash
     pipx install git+https://github.com/zettabrain/zettabrain-skills.git
     ```
     
     See [INSTALL-UBUNTU.md](INSTALL-UBUNTU.md) for detailed instructions.
     
     ### From Source
     ```bash
     git clone https://github.com/zettabrain/zettabrain-skills.git
     cd zettabrain-skills
     poetry install
     ```
     
     ## Quick Start
     
     ```bash
     # Install Ollama
     curl -fsSL https://ollama.com/install.sh | sh
     ollama serve
     ollama pull llama3.1:8b
     
     # Verify installation
     zbs version
     zbs check
     
     # Generate your first document
     zbs generate examples/simple-summarizer.md --input "your text here"
     ```
     
     ## What's Next
     
     See our [roadmap](README.md#roadmap) for upcoming features.
     
     ## Links
     
     - 📖 [Documentation](README.md)
     - 🐛 [Report Issues](https://github.com/zettabrain/zettabrain-skills/issues)
     - 💬 [Discussions](https://github.com/zettabrain/zettabrain-skills/discussions)
     ```
3. Click "Publish release"

### Via GitHub CLI

```bash
gh release create v0.1.0 \
  --title "ZettaBrain Skills v0.1.0 - Initial Release" \
  --notes "First public release of ZettaBrain Skills"
```

## Step 7: Set Up GitHub Actions (Optional)

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH
    
    - name: Install dependencies
      run: |
        poetry install
    
    - name: Run tests
      run: |
        poetry run pytest
    
    - name: Run linting
      run: |
        poetry run ruff check zettabrain-skills/
    
    - name: Check formatting
      run: |
        poetry run black --check zettabrain-skills/
```

Commit and push:

```bash
mkdir -p .github/workflows
# Create the file above
git add .github/workflows/tests.yml
git commit -m "Add GitHub Actions CI workflow"
git push
```

## Step 8: Create Documentation Pages

### Enable GitHub Pages

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main`, folder: `/(root)` or `/docs` if you create a docs folder
4. Save

### Create CONTRIBUTING.md

```bash
# Already created in repo, commit if not done
git add CONTRIBUTING.md
git commit -m "Add contributing guidelines"
git push
```

## Step 9: Add Repository Metadata

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```yaml
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11]
- ZettaBrain Skills version: [e.g., 0.1.0]
- Ollama version: [e.g., 0.1.20]

**Additional context**
Any other relevant information.
```

Create `.github/ISSUE_TEMPLATE/feature_request.md`:

```yaml
---
name: Feature request
about: Suggest an idea
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Any other context or screenshots.
```

## Step 10: Announce the Release

### On GitHub

1. Create a discussion: https://github.com/zettabrain/zettabrain-skills/discussions
2. Category: Announcements
3. Title: "ZettaBrain Skills v0.1.0 Released!"
4. Link to release notes

### Social Media (Optional)

- Twitter/X: Share repository link
- LinkedIn: Post about the release
- Reddit: r/Python, r/MachineLearning, r/LocalLLaMA
- Hacker News: Show HN post

## Quick Command Reference

```bash
# Clone and setup (for contributors)
git clone https://github.com/zettabrain/zettabrain-skills.git
cd zettabrain-skills
poetry install

# Development workflow
git checkout -b feature/my-feature
# Make changes
git add .
git commit -m "Add my feature"
git push origin feature/my-feature
# Create PR on GitHub

# Create new release
git tag v0.2.0
git push origin v0.2.0
gh release create v0.2.0 --generate-notes
```

## Verification Checklist

After publishing, verify:

- [ ] Repository is public and accessible
- [ ] README displays correctly with badges
- [ ] Installation instructions work (`pipx install git+...`)
- [ ] Examples are visible and downloadable
- [ ] Issues and Discussions are enabled
- [ ] Topics/tags are set
- [ ] License file is present
- [ ] GitHub Actions run successfully (if configured)
- [ ] Release v0.1.0 is published

## Post-Publishing Steps

1. **Update pip-installable package** (future):
   ```bash
   # Build package
   poetry build
   
   # Upload to PyPI
   poetry publish
   ```

2. **Update documentation links** in external locations

3. **Monitor Issues** for bug reports and questions

4. **Create project board** for tracking features

5. **Set up community**:
   - Code of Conduct
   - Security policy (SECURITY.md)
   - Governance model

## Troubleshooting

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/zettabrain/zettabrain-skills.git
```

### Error: "Permission denied (publickey)"

Use HTTPS instead of SSH, or set up SSH keys:
```bash
git remote set-url origin https://github.com/zettabrain/zettabrain-skills.git
```

### Error: "refusing to merge unrelated histories"

```bash
git pull origin main --allow-unrelated-histories
```

---

**Repository published!** 🎉

URL: https://github.com/zettabrain/zettabrain-skills

Install: `pipx install git+https://github.com/zettabrain/zettabrain-skills.git`
