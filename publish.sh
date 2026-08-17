#!/bin/bash

# ZettaBrainSkill Publishing Script
# This script will guide you through publishing to GitHub

set -e  # Exit on error

echo "🚀 ZettaBrainSkill Publishing Script"
echo "===================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Not in zettabrain-skills directory"
    echo "Please run this script from the zettabrain-skills directory"
    exit 1
fi

echo "✓ In correct directory"
echo ""

# Check git status
echo "📋 Checking git status..."
git status
echo ""

# Ask for confirmation
read -p "Do you want to commit all changes? (y/n) " -n 1 -r
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

# Show what will be committed
echo "📝 Files to be committed:"
git status --short
echo ""

# Commit
echo "💾 Creating commit..."
git commit -m "Initial release: ZettaBrainSkill v0.1.0

Core features:
- Skill parser and validator
- LLM provider abstraction (Ollama)
- Document generation engine
- CLI interface (zbs command)
- Example skills (summarizer, quotes)
- Comprehensive documentation
- Ubuntu installation via pipx/pip

Ready for production use."

echo "✓ Commit created"
echo ""

# Check if remote exists
if git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  Remote 'origin' already exists"
    echo "Current remote: $(git remote get-url origin)"
    read -p "Do you want to remove and re-add it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote remove origin
        echo "✓ Removed existing remote"
    fi
fi

# Add remote
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Adding GitHub remote..."
    git remote add origin https://github.com/zettabrain/zettabrain-skills.git
    echo "✓ Remote added"
fi

echo ""
echo "📤 Ready to push to GitHub"
echo ""
echo "IMPORTANT: Before pushing, make sure:"
echo "  1. You have created the repository on GitHub:"
echo "     https://github.com/organizations/zettabrain/repositories/new"
echo "  2. Repository name: zettabrain-skills"
echo "  3. Visibility: Public"
echo "  4. Do NOT initialize with README"
echo ""

read -p "Have you created the GitHub repository? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please create the repository first:"
    echo "1. Go to: https://github.com/organizations/zettabrain/repositories/new"
    echo "2. Name: zettabrain-skills"
    echo "3. Public repository"
    echo "4. Do NOT initialize"
    echo "5. Click 'Create repository'"
    echo ""
    echo "Then run this script again."
    exit 0
fi

# Rename branch to main
echo "🔀 Ensuring branch is named 'main'..."
git branch -M main
echo "✓ Branch renamed to main"
echo ""

# Push to GitHub
echo "📤 Pushing to GitHub..."
echo "You may be prompted for GitHub authentication..."
echo ""

if git push -u origin main; then
    echo ""
    echo "✅ Successfully published to GitHub!"
    echo ""
    echo "🎉 Next steps:"
    echo "1. View your repository: https://github.com/zettabrain/zettabrain-skills"
    echo "2. Create a release:"
    echo "   - Go to: https://github.com/zettabrain/zettabrain-skills/releases/new"
    echo "   - Tag: v0.1.0"
    echo "   - Title: ZettaBrainSkill v0.1.0 - Initial Release"
    echo "   - Click 'Publish release'"
    echo ""
    echo "3. Test installation:"
    echo "   pipx install git+https://github.com/zettabrain/zettabrain-skills.git"
    echo ""
else
    echo ""
    echo "❌ Push failed"
    echo ""
    echo "Common issues:"
    echo "1. Authentication failed - You may need to:"
    echo "   - Use GitHub personal access token"
    echo "   - Run: gh auth login (if you have GitHub CLI)"
    echo ""
    echo "2. Repository doesn't exist - Create it at:"
    echo "   https://github.com/organizations/zettabrain/repositories/new"
    echo ""
    echo "3. Permission denied - Make sure you have access to zettabrain org"
    exit 1
fi
