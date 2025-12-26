#!/bin/bash
# Quick update script to push the fixed workflow

echo "================================================"
echo "  Updating GitHub Actions Workflow"
echo "================================================"
echo ""
echo "Fixed: Updated to actions v4 (v3 is deprecated)"
echo ""

cd /app

# Add the updated file
git add .github/workflows/build.yml

# Commit
git commit -m "Fix: Update GitHub Actions to v4 (v3 deprecated)

- Update actions/checkout v3 -> v4
- Update actions/setup-python v4 -> v5  
- Update actions/upload-artifact v3 -> v4
- Fixes deprecation error"

echo ""
echo "Pushing to GitHub..."
git push

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Workflow updated on GitHub"
    echo ""
    echo "The build will now run correctly!"
    echo "Check: https://github.com/YOUR_USERNAME/YOUR_REPO/actions"
else
    echo ""
    echo "❌ Push failed. Run manually:"
    echo "   git push"
fi
