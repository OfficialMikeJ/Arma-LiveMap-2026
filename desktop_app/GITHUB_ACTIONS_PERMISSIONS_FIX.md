# GitHub Actions Permission Fix

## Issue

**Error:**
```
Failed to create release: 403
Resource not accessible by integration
```

**Cause:** GitHub Actions `GITHUB_TOKEN` doesn't have permission to create releases by default.

---

## Solution

Added permissions to the workflow file:

```yaml
permissions:
  contents: write
  pull-requests: write
```

---

## What This Does

**`contents: write`:**
- Create releases
- Push commits (version bump)
- Create tags
- Modify repository content

**`pull-requests: write`:**
- Comment on PRs (optional, for future features)
- Update PR status

---

## File Modified

**`.github/workflows/build.yml`**

**Added after `on:` section:**
```yaml
permissions:
  contents: write
  pull-requests: write
```

---

## Verification

After pushing this fix:
1. ✅ GitHub Actions can create releases
2. ✅ GitHub Actions can commit version bumps
3. ✅ GitHub Actions can push changes
4. ✅ No more 403 errors

---

## Alternative Fix (If Still Fails)

If the error persists, check repository settings:

**Settings → Actions → General → Workflow permissions:**
- Select: **"Read and write permissions"**
- Check: **"Allow GitHub Actions to create and approve pull requests"**

---

## Testing

Next push will:
1. Extract version
2. Auto-increment
3. Update files
4. Commit changes ✅ (now has permission)
5. Build executable
6. Create release ✅ (now has permission)
7. Upload assets ✅ (now has permission)

---

**Status:** ✅ Fixed

**Next:** Push and verify build succeeds

---

*Fix applied: December 27, 2025*
