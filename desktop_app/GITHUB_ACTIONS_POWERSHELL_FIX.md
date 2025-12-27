# GitHub Actions Build Fix - PowerShell Syntax Error

## Issue

**Error encountered:**
```
ParserError: Missing '(' after 'if' in if statement.
if exist desktop_app\docs\QUICKSTART.md copy ...
```

**Location:** GitHub Actions workflow, "Copy documentation to dist" step

---

## Root Cause

The workflow was using **CMD/DOS syntax** (`if exist`) in a step that runs **PowerShell** by default on Windows runners.

**Wrong syntax (CMD):**
```cmd
if exist file.txt copy file.txt destination\
```

**Correct syntax (PowerShell):**
```powershell
if (Test-Path file.txt) {
  Copy-Item file.txt destination\
}
```

---

## Solution

### Updated Workflow Step

**File:** `.github/workflows/build.yml`

**Before:**
```yaml
- name: Copy documentation to dist
  run: |
    copy desktop_app\README.md desktop_app\dist\ArmaReforgerMap\
    copy desktop_app\CHANGELOG.md desktop_app\dist\ArmaReforgerMap\
    if exist desktop_app\docs\QUICKSTART.md copy desktop_app\docs\QUICKSTART.md desktop_app\dist\ArmaReforgerMap\
```

**After:**
```yaml
- name: Copy documentation to dist
  shell: pwsh
  run: |
    Copy-Item desktop_app\README.md desktop_app\dist\ArmaReforgerMap\
    Copy-Item desktop_app\CHANGELOG.md desktop_app\dist\ArmaReforgerMap\
    if (Test-Path desktop_app\docs\QUICKSTART.md) {
      Copy-Item desktop_app\docs\QUICKSTART.md desktop_app\dist\ArmaReforgerMap\
    }
```

---

## Changes Made

1. **Explicitly specified shell:** `shell: pwsh` (PowerShell)
2. **Updated commands:**
   - `copy` → `Copy-Item`
   - `if exist` → `if (Test-Path file)`
3. **Added proper PowerShell syntax:**
   - Conditional blocks with `{ }`
   - Proper cmdlet names

---

## Why This Happened

GitHub Actions on Windows:
- Default shell: **PowerShell** (not CMD)
- PowerShell has different syntax than CMD
- `if exist` is CMD-specific, not PowerShell

---

## Verification

The workflow will now:
1. ✅ Copy README.md
2. ✅ Copy CHANGELOG.md
3. ✅ Check if QUICKSTART.md exists (PowerShell syntax)
4. ✅ Copy QUICKSTART.md if it exists
5. ✅ Continue with rest of build

---

## PowerShell Reference

**Common CMD → PowerShell conversions:**

| CMD | PowerShell |
|-----|------------|
| `copy` | `Copy-Item` |
| `move` | `Move-Item` |
| `del` | `Remove-Item` |
| `if exist file` | `if (Test-Path file)` |
| `mkdir` | `New-Item -ItemType Directory` |
| `dir` | `Get-ChildItem` |

---

## Files Modified

1. `.github/workflows/build.yml` - Fixed PowerShell syntax

---

## Expected Result

Next GitHub Actions build will:
- ✅ Extract version successfully (previous fix)
- ✅ Build executable with PyInstaller
- ✅ Copy documentation correctly
- ✅ Create release package
- ✅ Upload artifacts

---

**Status:** ✅ Fixed and ready for next push

**Next Steps:**
1. Push changes to GitHub
2. Monitor GitHub Actions build
3. Verify successful completion

---

*Fix applied: December 27, 2025*
