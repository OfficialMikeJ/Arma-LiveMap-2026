#!/bin/bash

# Quick Release Script
# Usage: ./quick_release.sh 0.100.030 "Release description"

set -e

if [ -z "$1" ]; then
    echo "Usage: ./quick_release.sh <version> [description]"
    echo "Example: ./quick_release.sh 0.100.030 \"Bug fixes and improvements\""
    exit 1
fi

VERSION=$1
DESCRIPTION=${2:-"Version $VERSION release"}

echo "======================================"
echo "Quick Release Script"
echo "======================================"
echo "Version: $VERSION"
echo "Description: $DESCRIPTION"
echo ""

# Step 1: Update version
echo "[1/5] Updating version in code..."
cd "$(dirname "$0")/.."
python scripts/update_version.py "$VERSION"

# Step 2: Stage changes
echo "[2/5] Staging changes..."
git add .

# Step 3: Commit
echo "[3/5] Committing..."
git commit -m "Release v$VERSION

$DESCRIPTION"

# Step 4: Create tag
echo "[4/5] Creating tag..."
git tag -a "v$VERSION" -m "Version $VERSION"

# Step 5: Push
echo "[5/5] Pushing to GitHub..."
git push origin main
git push origin "v$VERSION"

echo ""
echo "======================================"
echo "✅ Release initiated successfully!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Go to GitHub Actions to monitor build"
echo "2. Wait for build to complete (~5-10 minutes)"
echo "3. Check Releases tab for new release"
echo "4. Download and test the built executable"
echo ""
