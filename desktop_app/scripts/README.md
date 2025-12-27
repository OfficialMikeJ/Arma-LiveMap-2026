# Release Automation Scripts

This directory contains scripts for automating version management and GitHub releases.

## Scripts

### 1. `update_version.py`
Updates version numbers across the entire codebase.

**Usage:**
```bash
python update_version.py 0.100.030
```

**Updates:**
- `gui/main_window.py` - VERSION constant
- `gui/feedback_dialog.py` - version in feedback data
- `README.md` - current version badge
- `CHANGELOG.md` - version headers
- `versions.json` - version tracking

### 2. `create_github_release.py`
Creates GitHub releases with automatic changelog extraction.

**Usage:**
```bash
export GITHUB_TOKEN="your_token"
export GITHUB_REPOSITORY_OWNER="username"
export GITHUB_REPOSITORY="repo_name"
export RELEASE_VERSION="0.100.030"
export CHANGELOG_PATH="../CHANGELOG.md"
export ASSET_PATH="../release/ArmaReforgerMap.zip"

python create_github_release.py
```

**Environment Variables:**
- `GITHUB_TOKEN` - GitHub personal access token (auto-provided in Actions)
- `GITHUB_REPOSITORY_OWNER` - Repository owner username
- `GITHUB_REPOSITORY` - Repository name
- `RELEASE_VERSION` - Version to release
- `CHANGELOG_PATH` - Path to CHANGELOG.md
- `ASSET_PATH` - Path to .zip file to upload
- `PRERELEASE` - Set to 'true' for pre-release (optional)

### 3. `quick_release.sh` (Linux/Mac)
One-command release script.

**Usage:**
```bash
./quick_release.sh 0.100.030 "Bug fixes and improvements"
```

**What it does:**
1. Updates version in code
2. Commits changes
3. Creates git tag
4. Pushes to GitHub
5. Triggers GitHub Actions build

### 4. `quick_release.bat` (Windows)
Windows version of quick release script.

**Usage:**
```cmd
quick_release.bat 0.100.030 "Bug fixes and improvements"
```

## Workflow

### Option 1: Quick Release (Recommended)

**Linux/Mac:**
```bash
cd scripts
./quick_release.sh 0.100.030
```

**Windows:**
```cmd
cd scripts
quick_release.bat 0.100.030
```

This handles everything automatically.

### Option 2: Manual Steps

```bash
# 1. Update version
python scripts/update_version.py 0.100.030

# 2. Update CHANGELOG.md manually
vim CHANGELOG.md

# 3. Commit
git add .
git commit -m "Release v0.100.030"

# 4. Tag
git tag v0.100.030

# 5. Push
git push origin main --tags
```

### Option 3: GitHub Actions Manual Trigger

1. Go to repository on GitHub
2. Click **Actions** tab
3. Select **Build Arma Reforger Map Desktop App**
4. Click **Run workflow**
5. Set **Create release** to `true`
6. Click **Run workflow**

## Version Numbering

Format: `MAJOR.MINOR.PATCH`

Example: `0.100.030`
- `0` - Major version (pre-1.0 development)
- `100` - Minor version (feature milestone)
- `030` - Patch version (bug fixes)

## Planned Versions

From `versions.json`:

- **0.100.030** (2026) - Enhanced real-time functionality
- **0.103.045** (2026) - Voice chat integration
- **0.107.059** (2026) - Squad management
- **0.116.079** (2026) - Replay system
- **0.124.094** (2026) - Multi-language support

## Testing

Before releasing, always test locally:

```bash
# Build locally
cd desktop_app
pyinstaller --name "ArmaReforgerMap" --windowed main.py

# Test the executable
cd dist/ArmaReforgerMap
./ArmaReforgerMap.exe
```

## Troubleshooting

### "Version not found in code"

**Solution:** Ensure `VERSION = "x.x.x"` exists in `gui/main_window.py`

### "GitHub API error"

**Solution:** 
- Check `GITHUB_TOKEN` is valid
- Verify repository permissions
- Ensure repository exists

### "Release already exists"

**Solution:**
- Delete existing release/tag on GitHub
- Or increment version number

### "Asset upload failed"

**Solution:**
- Check file exists at `ASSET_PATH`
- Verify file is not too large (>2GB)
- Check network connection

## Files Modified

When running version update:
- `gui/main_window.py`
- `gui/feedback_dialog.py`
- `README.md`
- `CHANGELOG.md`
- `versions.json`

Always verify changes before committing.

## GitHub Actions Integration

The scripts integrate with `.github/workflows/build.yml`:

1. **Build** triggered by push/tag
2. **Extract version** from code
3. **Build executable** with PyInstaller
4. **Create release** (if tag push)
5. **Upload assets** to release

## Security Notes

- Never commit `GITHUB_TOKEN` to repository
- Use GitHub Actions secrets for automation
- Tokens are automatically provided in Actions environment

## Support

For detailed documentation, see:
- `docs/GITHUB_RELEASE_GUIDE.md` - Complete guide
- `.github/workflows/build.yml` - Workflow configuration
- `versions.json` - Version tracking

---

*Last Updated: December 27, 2025*
