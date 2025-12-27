# GitHub Actions Build Fix - Encoding Error

## Issue

**Error encountered:**
```
UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 6426: character maps to <undefined>
```

**Location:** GitHub Actions workflow, "Extract version from code" step

---

## Root Cause

The workflow was trying to read `gui/main_window.py` without specifying UTF-8 encoding. On Windows runners, Python defaults to `cp1252` encoding, which cannot decode Unicode characters like:

- `−` (minus sign) in "− Zoom Out"
- `⟲` (circular arrow) in "⟲ Reset"  
- `↻` (refresh symbol) in "↻ Refresh"
- `📝` (memo emoji) in "📝 Feedback"
- `⚙` (gear emoji) in "⚙ Settings"

---

## Solution

### 1. Created Dedicated Script

**File:** `/desktop_app/scripts/extract_version.py`

**Purpose:** Safely extract version with explicit UTF-8 encoding

**Usage:**
```bash
python scripts/extract_version.py gui/main_window.py
# Output: 0.099.024
```

**Features:**
- ✅ Explicit UTF-8 encoding
- ✅ Error handling
- ✅ Cross-platform compatible
- ✅ Regex-based version extraction

### 2. Updated Workflow

**File:** `.github/workflows/build.yml`

**Changed from:**
```yaml
VERSION=$(python -c "import re; content = open('gui/main_window.py').read(); ...")
```

**Changed to:**
```yaml
VERSION=$(python scripts/extract_version.py gui/main_window.py)
```

---

## Testing

```bash
cd /app/desktop_app
python scripts/extract_version.py gui/main_window.py
# ✓ Output: 0.099.024
```

---

## Files Modified

1. **New:** `/app/desktop_app/scripts/extract_version.py`
2. **Updated:** `.github/workflows/build.yml`

---

## Expected Result

Next GitHub Actions build will:
- ✅ Successfully extract version
- ✅ Handle Unicode characters correctly
- ✅ Build Windows executable
- ✅ Create artifacts

---

## Prevention

All Python files in the project use UTF-8 encoding. The workflow now explicitly handles this, preventing future encoding issues on Windows runners.

---

**Status:** ✅ Fixed and ready for next push

**Next Steps:**
1. Push changes to GitHub
2. Monitor GitHub Actions build
3. Verify successful completion

---

*Fix applied: December 27, 2025*
