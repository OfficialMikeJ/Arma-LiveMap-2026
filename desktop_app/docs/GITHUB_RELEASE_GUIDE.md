# GitHub Release Automation Guide

## Overview

This repository uses automated scripts to manage versioning and create GitHub releases when building the desktop application.

---

## Features

- ✅ **Automatic Version Detection** - Extracts version from code
- ✅ **GitHub Release Creation** - Auto-creates releases with changelog
- ✅ **Asset Upload** - Automatically uploads built .exe/.zip
- ✅ **Version Tracking** - Maintains version history in `versions.json`
- ✅ **Flexible Workflow** - Manual or automatic triggers

---

## How It Works

### 1. Version Management

Version is defined in `/desktop_app/gui/main_window.py`:

```python
VERSION = "0.100.030"
```

### 2. Build Workflow

When you push to GitHub:

1. **GitHub Actions** triggers the build workflow
2. **PyInstaller** builds the Windows executable
3. **Version** is extracted from code automatically
4. **ZIP archive** is created with version number
5. **GitHub Release** is created (if configured)
6. **Assets** are uploaded to the release

---

## Usage

### Method 1: Automatic Release (Tag Push)

Create and push a git tag:

```bash
# Update version in code first
cd desktop_app/scripts
python update_version.py 0.100.030

# Commit changes
git add .
git commit -m "Bump version to 0.100.030"

# Create and push tag
git tag v0.100.030
git push origin main
git push origin v0.100.030
```

GitHub Actions will:
- Build the application
- Create release `v0.100.030`
- Upload the .zip file
- Extract release notes from CHANGELOG.md

### Method 2: Manual Workflow Dispatch

1. Go to GitHub repository
2. Click **Actions** tab
3. Select **Build Arma Reforger Map Desktop App**
4. Click **Run workflow**
5. Choose options:
   - Branch: `main`
   - Create release: `true`
6. Click **Run workflow**

### Method 3: Regular Push (Build Only)

```bash
git add .
git commit -m "Your changes"
git push origin main
```

This will:
- Build the application
- Upload artifacts
- **NOT** create a release

---

## Scripts

### 1. Update Version (`scripts/update_version.py`)

Updates version across all files:

```bash
cd desktop_app/scripts
python update_version.py 0.100.030
```

**Updates:**
- `gui/main_window.py` - VERSION constant
- `gui/feedback_dialog.py` - version field
- `README.md` - current version
- `CHANGELOG.md` - version header
- `versions.json` - version tracking

### 2. Create GitHub Release (`scripts/create_github_release.py`)

Manually create a release:

```bash
export GITHUB_TOKEN="your_token"
export GITHUB_REPOSITORY_OWNER="your_username"
export GITHUB_REPOSITORY="your_repo"
export RELEASE_VERSION="0.100.030"
export CHANGELOG_PATH="CHANGELOG.md"
export ASSET_PATH="path/to/file.zip"

python scripts/create_github_release.py
```

---

## Version Configuration

### `versions.json`

Tracks current and upcoming versions:

```json
{
  "current_version": "0.099.024",
  "upcoming_versions": [
    {
      "version": "0.100.030",
      "year": 2026,
      "status": "planned",
      "features": ["Feature 1", "Feature 2"]
    }
  ]
}
```

### Planned Versions

- **0.100.030** (2026) - Enhanced real-time functionality
- **0.103.045** (2026) - Voice chat integration
- **0.107.059** (2026) - Squad management
- **0.116.079** (2026) - Replay system
- **0.124.094** (2026) - Multi-language support

---

## Release Workflow

### Step-by-Step: Releasing a New Version

#### 1. Prepare Release

```bash
# Update CHANGELOG.md
vim CHANGELOG.md  # Add new version section

# Update version in code
cd scripts
python update_version.py 0.100.030

# Verify changes
grep -r "0.100.030" ../
```

#### 2. Commit and Tag

```bash
git add .
git commit -m "Release v0.100.030

- Feature 1
- Feature 2
- Bug fixes"

git tag -a v0.100.030 -m "Version 0.100.030"
```

#### 3. Push to GitHub

```bash
git push origin main
git push origin v0.100.030
```

#### 4. Monitor Build

1. Go to GitHub Actions
2. Watch the build progress
3. Wait for completion (~5-10 minutes)

#### 5. Verify Release

1. Go to **Releases** tab
2. Verify release created: `v0.100.030`
3. Check release notes
4. Download and test the .zip file

---

## CHANGELOG Format

For automatic release notes extraction, use this format:

```markdown
## [0.100.030] - 2026-XX-XX

### Added
- Feature 1
- Feature 2

### Fixed
- Bug 1
- Bug 2

### Changed
- Change 1
```

The script will extract everything between version headers.

---

## Troubleshooting

### Release Not Created

**Problem:** Build succeeded but no release

**Solution:**
- Check if tag was pushed: `git push origin v0.100.030`
- Verify GitHub Actions workflow has `GITHUB_TOKEN` permission
- Check workflow logs for errors

### Wrong Version in Release

**Problem:** Release shows old version

**Solution:**
- Verify `VERSION` in `gui/main_window.py` is updated
- Check `versions.json` current_version
- Rebuild and push again

### Asset Not Uploaded

**Problem:** Release exists but no .zip file

**Solution:**
- Check build step completed successfully
- Verify ZIP was created in `release/` folder
- Check workflow logs for upload errors

### Release Notes Empty

**Problem:** Release created with no description

**Solution:**
- Add version section to `CHANGELOG.md`
- Use format: `## [0.100.030]`
- Ensure changelog is committed before tagging

---

## Advanced Usage

### Pre-release Versions

Create a pre-release:

```bash
# Tag with -alpha, -beta, or -rc suffix
git tag v0.100.030-beta
git push origin v0.100.030-beta
```

Or set in workflow:

```bash
export PRERELEASE=true
python scripts/create_github_release.py
```

### Custom Release Notes

Override automatic extraction:

```bash
export RELEASE_NOTES="Custom release notes here"
python scripts/create_github_release.py
```

### Multiple Assets

Upload additional files:

```python
from scripts.create_github_release import GitHubReleaseManager

manager = GitHubReleaseManager(owner, repo, token)
release = manager.create_release(version, notes)

manager.upload_asset(release['id'], 'file1.zip')
manager.upload_asset(release['id'], 'file2.exe')
manager.upload_asset(release['id'], 'CHANGELOG.md')
```

---

## GitHub Actions Configuration

### Required Secrets

**Automatic:** `GITHUB_TOKEN` is provided by GitHub Actions

**Optional:** None required for basic usage

### Permissions

Ensure repository settings allow:
- Actions to create releases
- Workflow has write permissions

**Settings → Actions → General → Workflow permissions:**
- ☑ Read and write permissions

---

## Best Practices

1. **Update CHANGELOG First**
   - Add version section before bumping version
   - Include all changes since last release

2. **Test Before Release**
   - Build locally first
   - Test the executable
   - Verify all features work

3. **Semantic Versioning**
   - Follow pattern: `MAJOR.MINOR.PATCH`
   - Increment appropriately

4. **Tag Format**
   - Always prefix with `v`: `v0.100.030`
   - Use same version as in code

5. **Descriptive Commits**
   - Write clear commit messages
   - Reference issue numbers

---

## Quick Reference

```bash
# Update version
python scripts/update_version.py 0.100.030

# Commit and tag
git add .
git commit -m "Release v0.100.030"
git tag v0.100.030

# Push everything
git push origin main --tags

# Monitor build
# Go to GitHub Actions tab

# Verify release
# Go to Releases tab
```

---

## Support

For issues or questions:
- Check GitHub Actions logs
- Review CHANGELOG.md format
- Verify version in code matches tag
- Check GitHub repository permissions

---

*Last Updated: December 27, 2025*
