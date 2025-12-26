#!/bin/bash
# Quick Push Script for Arma Reforger Map

echo "================================================"
echo "  Arma Reforger Map - GitHub Push Script"
echo "================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "desktop_app/main.py" ]; then
    echo "❌ Error: Run this script from /app directory"
    echo "   cd /app && ./push_to_github.sh"
    exit 1
fi

echo "✓ Correct directory"
echo ""

# Check if .github exists at root
if [ ! -f ".github/workflows/build.yml" ]; then
    echo "❌ Error: .github/workflows/build.yml not found at root"
    echo "   The workflow file must be at repository root!"
    exit 1
fi

echo "✓ GitHub Actions workflow found at root"
echo ""

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git branch -M main
    echo "✓ Git initialized"
    echo ""
fi

# Show what will be added
echo "Files to be committed:"
echo "  - .github/workflows/build.yml (GitHub Actions)"
echo "  - desktop_app/ (Your application)"
echo "  - Documentation files"
echo ""

# Ask for GitHub repository URL
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ Error: Repository URL is required"
    exit 1
fi

echo ""
echo "Setting up remote..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

echo "✓ Remote set to: $REPO_URL"
echo ""

# Add files
echo "Adding files to git..."
git add .github/
git add desktop_app/
git add GITHUB_ACTIONS_FIX.md
git add README.md 2>/dev/null || true
git add .gitignore 2>/dev/null || true

echo "✓ Files added"
echo ""

# Commit
echo "Creating commit..."
git commit -m "Add Arma Reforger Live Interactive Map with GitHub Actions

- Desktop application with PySide6
- Live map with real-time markers
- TOTP/QR authentication
- Server management (6 servers)
- GitHub Actions for automatic .exe builds"

echo "✓ Commit created"
echo ""

# Push
echo "Pushing to GitHub..."
echo ""
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "  ✅ SUCCESS!"
    echo "================================================"
    echo ""
    echo "Your code is now on GitHub!"
    echo ""
    echo "Next steps:"
    echo "  1. Go to your GitHub repository"
    echo "  2. Click the 'Actions' tab"
    echo "  3. Wait 5-10 minutes for the build"
    echo "  4. Download artifacts when complete"
    echo ""
    echo "Your GitHub repo: ${REPO_URL%.git}"
    echo "Actions URL: ${REPO_URL%.git}/actions"
    echo ""
else
    echo ""
    echo "================================================"
    echo "  ❌ PUSH FAILED"
    echo "================================================"
    echo ""
    echo "Common issues:"
    echo "  - Authentication: Use Personal Access Token (not password)"
    echo "  - Permissions: Check you have write access to repo"
    echo "  - Remote URL: Verify the repository URL is correct"
    echo ""
    echo "Try manually:"
    echo "  git push -u origin main"
    echo ""
fi
