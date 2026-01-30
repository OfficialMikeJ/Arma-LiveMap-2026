# Auto-Increment Versioning System

## Overview

Every push to `main` branch automatically:
1. ✅ Increments patch version (0.099.024 → 0.099.025)
2. ✅ Updates version in code
3. ✅ Commits the version bump
4. ✅ Builds Windows executable
5. ✅ Creates GitHub Release
6. ✅ Uploads .zip file

---

## How It Works

### Automatic Workflow

```
You push code → GitHub Actions triggered
                ↓
         Extract current version (0.099.024)
                ↓
         Auto-increment (+1 to patch)
                ↓
         New version: 0.099.025
                ↓
         Update version in code
                ↓
         Commit: "chore: bump version to 0.099.025"
                ↓
         Build Windows .exe
                ↓
         Create Release v0.099.025
                ↓
         Upload ArmaReforgerMap-v0.099.025-Windows-Portable.zip
```

---

## Version Numbering

### Format: `MAJOR.MINOR.PATCH`

**Example: 0.099.024**
- `0` - Major version (pre-1.0)
- `099` - Minor version (feature milestone)
- `024` - Patch version (auto-incremented)

### Auto-Increment Rules

**Patch versions (automatic):**
```
0.099.024 → 0.099.025 → 0.099.026 → 0.099.027 ...
```

**Minor versions (manual, monthly):**
```
0.099.xxx → 0.100.030  (January 2026)
0.100.xxx → 0.103.045  (February 2026)
0.103.xxx → 0.107.059  (March 2026)
```

---

## Your Workflow

### Daily Development

```bash
# Make changes to code
vim desktop_app/gui/main_window.py

# Commit your changes
git add .
git commit -m "feat: add new marker type"

# Push to GitHub
git push origin main
```

**GitHub Actions will automatically:**
1. Increment version: 0.099.024 → 0.099.025
2. Build the app
3. Create release v0.099.025
4. Upload the .zip

**You get:** New release in GitHub with incremented version!

---

## Monthly Major Updates

### End of Month Process

When you're ready to move to the next major version (e.g., 0.100.030):

**Option 1: Manual Update**
```bash
cd desktop_app/scripts
python update_version.py 0.100.030
git add .
git commit -m "chore: release v0.100.030"
git push origin main
```

**Option 2: Let me know**
Just say: *"Ready to update to version 0.100.030"*

I'll handle the version update for you.

---

## Commit Message Format

### Your Commits (manual):
```bash
git commit -m "feat: add voice chat integration"
git commit -m "fix: marker sync issue"
git commit -m "docs: update README"
```

### Bot Commits (automatic):
```
chore: bump version to 0.099.025 [skip ci]
```

The `[skip ci]` prevents infinite loops - the bot's commit won't trigger another build.

---

## Release Management

### Automatic Releases

Every push creates a new release:

```
Releases Tab:
├── v0.099.027 (Latest)
├── v0.099.026
├── v0.099.025
├── v0.099.024
└── v0.099.023
```

Each release contains:
- Release notes from CHANGELOG.md
- `ArmaReforgerMap-v0.099.027-Windows-Portable.zip`
- Download count tracking
- Release date

### Accessing Releases

1. Go to your GitHub repository
2. Click **Releases** tab
3. Latest version is always at the top
4. Download the .zip file
5. Users always get the newest build

---

## Version Tracking

### In Code

**`gui/main_window.py`:**
```python
VERSION = "0.099.025"  # Auto-updated
```

**`gui/feedback_dialog.py`:**
```python
'version': '0.099.025'  # Auto-updated
```

### In Repository

**`versions.json`:**
```json
{
  "current_version": "0.099.025",
  "version_history": [
    {"version": "0.099.025", "date": "2025-12-27"},
    {"version": "0.099.024", "date": "2025-12-27"}
  ]
}
```

---

## Preventing Infinite Loops

### The Problem

Without protection:
```
Push → Build → Commit version → Push → Build → Commit → ...
```

### The Solution

1. **[skip ci] in commit message**
   ```
   chore: bump version to 0.099.025 [skip ci]
   ```
   GitHub Actions ignores commits with `[skip ci]`

2. **Bot identification**
   ```yaml
   git config user.name "github-actions[bot]"
   ```
   Clear identification of automated commits

---

## Examples

### Example 1: Bug Fix

```bash
# You: Fix a bug
git commit -m "fix: websocket reconnection issue"
git push

# GitHub Actions:
# Current: 0.099.024 → New: 0.099.025
# Creates release v0.099.025
# Uploads ArmaReforgerMap-v0.099.025-Windows-Portable.zip
```

### Example 2: New Feature

```bash
# You: Add feature
git commit -m "feat: add squad management"
git push

# GitHub Actions:
# Current: 0.099.025 → New: 0.099.026
# Creates release v0.099.026
```

### Example 3: Monthly Update

```bash
# You: End of month, major update
python scripts/update_version.py 0.100.030
git commit -m "chore: release v0.100.030 - Enhanced real-time features"
git push

# GitHub Actions:
# Current: 0.100.030 → New: 0.100.031 (next push)
# Creates release v0.100.030
```

---

## Monitoring

### Check Build Status

1. Go to **Actions** tab
2. See latest workflow run
3. Green ✓ = Success
4. Red ✗ = Failed

### Check Releases

1. Go to **Releases** tab
2. See latest version
3. Download count visible
4. Click to download .zip

### Version History

```bash
# View version history
cat desktop_app/versions.json

# Check current version
grep VERSION desktop_app/gui/main_window.py
```

---

## Benefits

✅ **No manual version management**
- Push code, version auto-increments
- No need to remember to update version

✅ **Every push = new release**
- Users always have access to latest
- Clear version progression
- Full download history

✅ **Automatic changelogs**
- Release notes from CHANGELOG.md
- Professional release management

✅ **Version tracking**
- All versions documented
- Easy rollback if needed
- Clear development timeline

---

## Notes

### When Auto-Increment Happens

- ✅ Push to `main` branch
- ❌ Pull requests (no increment)
- ❌ Pushes to other branches
- ✅ Manual workflow dispatch

### Commit Message Convention

While not required, consider:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation
- `chore:` - Maintenance
- `refactor:` - Code restructuring

### Monthly Version Updates

Remember to manually update to major versions:
- Current: 0.099.xxx (patch auto-increments)
- Next: 0.100.030 (manual update when ready)
- Then: 0.103.045 (manual, next month)

I'll remind you and help with the update!

---

## Troubleshooting

### "No version change detected"

**Solution:** The auto-increment only runs on push to main

### "Release already exists"

**Solution:** Delete the release on GitHub and re-run

### "Build failed"

**Solution:** Check Actions tab for error logs

---

**Status:** ✅ Auto-increment system active!

**Next push will create version 0.099.025**

---

*Last Updated: December 27, 2025*
