# Quick Fix Guide - GitHub Actions 403 Error

## Problem
```
Failed to create release: 403
Resource not accessible by integration
```

---

## Solution (2 Steps)

### Step 1: Update Workflow File ✅ (Already Done)

The workflow file has been updated with permissions.

### Step 2: Check Repository Settings

**You need to verify repository permissions:**

1. Go to your GitHub repository
2. Click **Settings** (top right)
3. Click **Actions** → **General** (left sidebar)
4. Scroll to **"Workflow permissions"**
5. Select: **"Read and write permissions"**
6. Check: ☑️ **"Allow GitHub Actions to create and approve pull requests"**
7. Click **Save**

---

## Visual Guide

```
GitHub Repository
└─ Settings
   └─ Actions
      └─ General
         └─ Workflow permissions
            ├─ (•) Read and write permissions  ← SELECT THIS
            │   └─ [✓] Allow GitHub Actions to create and approve pull requests
            │
            └─ [ Save ]  ← CLICK THIS
```

---

## After Fixing

Push your code:
```bash
git add .
git commit -m "fix: add workflow permissions for releases"
git push origin main
```

The build will now:
- ✅ Create releases (403 error fixed)
- ✅ Commit version bumps
- ✅ Upload assets

---

## If Still Fails

Contact me and I'll help debug further. But this should fix it!

---

**Status:** Ready to test after you update repository settings

**Time to fix:** < 1 minute in GitHub settings
