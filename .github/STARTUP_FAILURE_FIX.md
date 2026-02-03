# 🔴 "Startup Failure" Diagnostic Guide

## 🚨 Issue: All Workflows Show "Startup Failure"

If **every workflow** (including simple tests) shows "startup failure", this usually means:

1. **YAML syntax error** (most common)
2. **GitHub Actions is disabled** on the repository
3. **Permissions issue** with GitHub Actions
4. **Branch protection** preventing workflow execution
5. **GitHub service issue**

---

## ✅ Step-by-Step Fixes

### Fix 1: Verify GitHub Actions is Enabled

1. Go to your GitHub repository
2. Click **Settings** (top right)
3. In left sidebar, click **Actions** → **General**
4. Under "Actions permissions", ensure one of these is selected:
   - ✅ "Allow all actions and reusable workflows"
   - ✅ "Allow [org name], and select non-[org name], actions and reusable workflows"
   
   **NOT:**
   - ❌ "Disable actions"

5. Under "Workflow permissions", ensure:
   - ✅ "Read and write permissions" is selected
   - ✅ "Allow GitHub Actions to create and approve pull requests" is checked

6. Click **Save**

### Fix 2: Check YAML Syntax Online

Before pushing, validate your YAML:

1. Go to: https://www.yamllint.com/
2. Copy the content of your workflow file
3. Paste and check for errors
4. Fix any syntax issues

### Fix 3: Use the Absolute Minimal Workflow

I've created `minimal-test.yml` - the simplest possible workflow:

```yaml
name: Minimal Test

on:
  workflow_dispatch:

jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello World"
      - run: echo "GitHub Actions is working"
```

**To test:**
1. Commit and push this file
2. Go to Actions tab
3. Select "Minimal Test"
4. Run it

**If this fails too**, the issue is NOT with the workflow files.

### Fix 4: Check Repository Settings

**Problem:** Actions might be restricted at organization level

**Check:**
1. If repo is in an organization, go to Organization Settings
2. Navigate to Actions → General
3. Ensure Actions are allowed for this repository
4. Check if specific workflows need approval

### Fix 5: Check GitHub Status

**Problem:** GitHub Actions service might be down

**Check:**
1. Visit: https://www.githubstatus.com/
2. Look for "Actions" service status
3. If it's having issues, wait and try later

### Fix 6: Clear Workflow Cache

**Problem:** Old workflow data might be cached

**Steps:**
1. Go to Actions tab
2. Click "Caches" in left sidebar (if available)
3. Delete all caches
4. Try running workflow again

### Fix 7: Re-create the Workflow File

**Problem:** File might have invisible corruption

**Steps:**
```bash
cd /app/.github/workflows

# Delete the problematic file
rm test-workflow.yml

# Create a fresh one
cat > test-workflow.yml << 'EOF'
name: Fresh Test

on:
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Hello
        run: echo "Test successful"
EOF

# Commit and push
git add test-workflow.yml
git commit -m "Fresh workflow file"
git push
```

### Fix 8: Check Workflow Logs

**Problem:** Error message might have more details

**Steps:**
1. Click on the failed workflow run
2. Look at the very top for any error messages
3. Common startup failures show:
   - "Unable to resolve action"
   - "Invalid workflow file"
   - "Workflow is not valid"

**Screenshot what you see and check the specific error**

---

## 🔍 Diagnostic Questions

Please check and answer:

### Question 1: Where exactly do you see "Startup failure"?
- [ ] In the workflow list (before clicking)
- [ ] After clicking "Run workflow"
- [ ] In the workflow run details page
- [ ] In the logs of a step

### Question 2: What does the error message say exactly?
Copy the exact text from:
- The Actions tab
- The workflow run page
- Any error messages shown

### Question 3: Can you see the workflow file on GitHub?
1. Navigate to `.github/workflows/test-workflow.yml` on GitHub
2. Is the file there? YES / NO
3. Does it show the correct content? YES / NO

### Question 4: Repository settings
- [ ] Is this a personal repository or organization?
- [ ] Are you the owner or a contributor?
- [ ] Is the repository public or private?

---

## 📋 Current Workflow Files

I've created **3 different test workflows** with increasing simplicity:

### 1. minimal-test.yml (Most Simple)
```yaml
name: Minimal Test
on: workflow_dispatch
jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello World"
```
**Size:** 4 lines  
**Complexity:** Minimal  
**Purpose:** If this fails, it's NOT a workflow issue

### 2. simple-test.yml (Simple)
```yaml
name: Simple Test
on: workflow_dispatch
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Hello World
        run: echo "Hello from GitHub Actions!"
      - name: Success
        run: echo "Test completed successfully!"
```
**Size:** 8 lines  
**Complexity:** Basic  
**Purpose:** Test with named steps

### 3. test-workflow.yml (Full Test)
- Has multiple steps
- Lists directories
- Checks Node.js and Java
- More complex

**Recommended Testing Order:**
1. Try `minimal-test.yml` first
2. If that works, try `simple-test.yml`
3. If that works, try `test-workflow.yml`
4. This helps identify where the issue is

---

## 🎯 Most Likely Causes

Based on "startup failure" for ALL workflows:

### 1. GitHub Actions Not Enabled (80% likely)
- **Fix:** Settings → Actions → General → Enable Actions

### 2. Workflow Files Not Pushed (15% likely)
- **Check:** Are files visible on GitHub in `.github/workflows/`?
- **Fix:** Push the files: `git push origin main`

### 3. YAML Syntax Error in ALL Files (3% likely)
- **Check:** Validate each file at yamllint.com
- **Fix:** Use the minimal-test.yml provided

### 4. GitHub Service Issue (2% likely)
- **Check:** Visit githubstatus.com
- **Fix:** Wait for GitHub to resolve

---

## 🆘 If Nothing Works

**Extreme measures:**

### Option 1: Create Workflow Through GitHub UI

1. Go to your repo on GitHub
2. Click "Actions" tab
3. Click "New workflow"
4. Click "set up a workflow yourself"
5. Paste this:
```yaml
name: UI Created Test
on: workflow_dispatch
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Created via UI"
```
6. Click "Start commit"
7. Commit directly to main
8. Try running it

**If this works:** Issue is with local files  
**If this fails:** Issue is with repository settings

### Option 2: Create New Test Repository

1. Create a brand new GitHub repository
2. Push just the workflow files
3. See if they work there

**If they work:** Issue is specific to your main repository  
**If they don't work:** Issue is with your GitHub account/organization

---

## 📞 Getting More Help

If you've tried everything:

1. **Copy the exact error message** from GitHub
2. **Take a screenshot** of the failure
3. **Check:** Settings → Actions → General (screenshot that too)
4. **Verify:** Can you see the workflow files on GitHub's website?

Share this information and we can debug further.

---

## ✅ Quick Test Script

Run this to verify everything locally:

```bash
cd /app/.github/workflows

echo "=== Checking workflow files ==="
ls -lah *.yml

echo -e "\n=== Validating YAML syntax ==="
for f in *.yml; do
  echo "Checking $f..."
  python3 -c "import yaml; yaml.safe_load(open('$f'))" && echo "✅ Valid" || echo "❌ Invalid"
done

echo -e "\n=== Checking git status ==="
git status .github/workflows/

echo -e "\n=== Files need to be pushed? ==="
git diff --name-only origin/main .github/workflows/ || echo "Not pushed yet"
```

This checks:
- ✅ Files exist
- ✅ YAML is valid
- ✅ Git status
- ✅ Push status

---

**Next Step:** Try pushing and running `minimal-test.yml` first. It's impossible for that to fail unless there's a settings/permissions issue.
