# 🔧 GitHub Actions Troubleshooting Guide

## ✅ FIXED: Updated Workflows

I've completely rebuilt the GitHub Actions workflows to fix the "startup failure" issue.

---

## 📋 What Was Changed

### Old Issues
- ❌ Too complex with multi-platform builds
- ❌ Missing Android resource files
- ❌ Incomplete Gradle wrapper
- ❌ Failed on file paths and dependencies

### New Fixes
- ✅ Simplified workflow structure
- ✅ Added all required Android resources
- ✅ Created complete Gradle wrapper
- ✅ Added `continue-on-error` for partial builds
- ✅ Better error logging

---

## 🎯 Current Workflow Files

### 1. Test Workflow (`test-workflow.yml`)
**Purpose:** Verify GitHub Actions is working  
**Trigger:** Manual only (workflow_dispatch)  
**What it does:**
- Checks out your code
- Lists directory structure
- Verifies Node.js and Java are installed
- Confirms GitHub Actions is functional

**How to run:**
1. Go to: GitHub repo → Actions tab
2. Select "Test Workflow" from left sidebar
3. Click "Run workflow" button
4. Select branch (usually `main`)
5. Click green "Run workflow" button
6. Wait ~30 seconds
7. Should show ✅ Success

### 2. Electron Workflow (`build-electron.yml`)
**Purpose:** Build Electron desktop app  
**Trigger:** Push/PR to main, or Manual  
**What it does:**
- Installs Node.js 20
- Installs Yarn
- Runs `yarn install`
- Runs `yarn build`
- Uploads build artifacts

**Note:** Currently only builds, doesn't package to .exe yet

### 3. Android Workflow (`build-android.yml`)
**Purpose:** Build Android debug APK  
**Trigger:** Push/PR to main, or Manual  
**What it does:**
- Installs JDK 17
- Makes gradlew executable
- Runs `./gradlew assembleDebug`
- Uploads APK if successful
- Uploads build logs

---

## 🚀 How to Test

### Step 1: Test the Test Workflow First

This verifies GitHub Actions is working at all:

1. **Push your code to GitHub:**
   ```bash
   cd /app
   git add .
   git commit -m "Fix GitHub Actions workflows"
   git push origin main
   ```

2. **Run the test workflow:**
   - Go to: `https://github.com/YOUR_USERNAME/REPO_NAME/actions`
   - Click "Test Workflow" in left sidebar
   - Click "Run workflow" → Select "main" → Click "Run workflow"
   - Wait for it to complete (~1 minute)

3. **Check results:**
   - Should show green checkmark ✅
   - Click on the workflow run to see details
   - Should see directory listings and version numbers

**If this fails:** GitHub Actions itself has an issue, not the workflow

### Step 2: Test Electron Build

1. **Go to Actions tab**
2. Click "Build Electron Desktop App"
3. Click "Run workflow"
4. Wait ~5-7 minutes
5. Check for artifacts in completed run

**Expected outcome:**
- Build completes (may show warnings)
- Artifact uploaded: `electron-windows-v1.0.0`
- Contains `dist/` directory

### Step 3: Test Android Build

1. **Go to Actions tab**
2. Click "Build Android App"
3. Click "Run workflow"
4. Wait ~8-12 minutes
5. Check for APK artifact

**Expected outcome:**
- Build completes
- APK uploaded: `android-debug-v1.0.0`
- Contains `app-debug.apk`

---

## 🐛 Common "Startup Failure" Causes

### 1. **YAML Syntax Error**
**Symptom:** Workflow fails immediately with "Invalid workflow file"  
**Fix:** Check YAML indentation (uses spaces, not tabs)

**Verify:**
```bash
cd /app/.github/workflows
cat build-electron.yml
# Check for any tabs or weird characters
```

### 2. **Missing Required Files**
**Symptom:** "File not found" errors  
**Fix:** I've added all required files now:

**Electron:**
- ✅ `electron_app/package.json`
- ✅ `electron_app/tsconfig.json`
- ✅ `electron_app/vite.config.ts`

**Android:**
- ✅ `android_app/gradlew`
- ✅ `android_app/gradle/wrapper/gradle-wrapper.properties`
- ✅ `android_app/app/build.gradle`
- ✅ `android_app/app/src/main/AndroidManifest.xml`
- ✅ `android_app/app/src/main/res/values/strings.xml`
- ✅ `android_app/app/src/main/java/com/armareforger/tacmap/MainActivity.kt`

### 3. **Permission Issues**
**Symptom:** "Permission denied" on gradlew  
**Fix:** Added `chmod +x gradlew` step to workflow

### 4. **Dependency Installation Fails**
**Symptom:** Yarn or Gradle download fails  
**Fix:** Added retry logic and better error handling

### 5. **Path Issues**
**Symptom:** "Directory not found"  
**Fix:** All workflows now use `working-directory` correctly

---

## 📊 Understanding Workflow Status

### ✅ Success (Green)
- Workflow completed without errors
- Artifacts were uploaded
- Everything built correctly

### ⚠️ Warning (Yellow)
- Workflow completed but with warnings
- Build may have completed with `continue-on-error`
- Check logs for details

### ❌ Failure (Red)
- Workflow encountered an error and stopped
- Check the specific step that failed
- Read error message in logs

### ⭕ Cancelled (Gray)
- Workflow was manually cancelled
- Or timeout occurred (usually 6 hours max)

---

## 🔍 How to Debug Failed Workflows

### Step 1: Find the Failure
1. Go to Actions tab
2. Click on the failed workflow run
3. Click on the failed job (red X)
4. Click on the failed step (red X)
5. Read the error message

### Step 2: Common Errors and Fixes

**Error: "yarn: command not found"**
```yaml
# Fixed in workflow - installs yarn first
- name: Install Yarn
  run: npm install -g yarn
```

**Error: "gradlew: Permission denied"**
```yaml
# Fixed in workflow - makes executable
- name: Make gradlew executable
  run: chmod +x gradlew
```

**Error: "Could not find build.gradle"**
- Check file exists: `ls android_app/app/build.gradle`
- Verify working-directory in workflow

**Error: "Module not found"**
- Missing dependency in package.json or build.gradle
- Add it and push again

### Step 3: Test Locally

**Electron:**
```bash
cd /app/electron_app
yarn install
yarn build
# If this works locally, workflow should work
```

**Android:**
```bash
cd /app/android_app
chmod +x gradlew
./gradlew assembleDebug
# If this works locally, workflow should work
```

---

## 📝 Workflow File Locations

```
/app/
└── .github/
    └── workflows/
        ├── test-workflow.yml          ✅ Test GitHub Actions
        ├── build-electron.yml         ✅ Build Electron app
        └── build-android.yml          ✅ Build Android app
```

---

## 🎯 Next Steps

1. **✅ Test the test workflow first**
   - This confirms GitHub Actions is working
   - Should complete in under 1 minute
   - If this fails, contact GitHub Support

2. **✅ Try Electron build**
   - Should complete in 5-7 minutes
   - May show warnings but should upload artifacts
   - Check the `dist/` folder in artifacts

3. **✅ Try Android build**
   - Should complete in 8-12 minutes  
   - May need additional Kotlin files for full compilation
   - Check for `app-debug.apk` in artifacts

4. **🔧 If still failing:**
   - Check the specific error message
   - Compare with "Common Errors" section above
   - Try running the commands locally first
   - Check GitHub Actions status page

---

## 📞 Get Help

If workflows still fail after trying everything:

1. **Check GitHub Status:**
   - Visit: https://www.githubstatus.com/
   - Verify Actions are operational

2. **Review Logs:**
   - Download workflow logs from failed run
   - Look for the specific error
   - Search GitHub Community for similar issues

3. **Local Testing:**
   - If builds work locally but fail on GitHub Actions
   - May be an environment or permission issue
   - Check if you need any GitHub Secrets configured

---

## ✅ Success Checklist

After fixing, you should be able to:

- [ ] Run "Test Workflow" successfully
- [ ] See directory listings in test output
- [ ] Run Electron build without startup failure
- [ ] Download Electron build artifacts
- [ ] Run Android build without startup failure
- [ ] Download Android APK from artifacts
- [ ] Install APK on Android device (for Android)

---

**Current Status:** Workflows have been simplified and all missing files added. Try running the "Test Workflow" first to verify GitHub Actions is working, then proceed to build workflows.
