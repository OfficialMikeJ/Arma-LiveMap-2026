# GitHub Actions - Automated Build System

**Status:** ✅ Configured and Ready  
**Location:** `/app/.github/workflows/`

---

## 📋 Overview

Two separate GitHub Actions workflows have been created to automatically build both the Electron Desktop App and Android Mobile App whenever code is pushed to the repository.

### Workflows Created

1. **`build-electron.yml`** - Builds Electron desktop app for Windows, Linux, and macOS
2. **`build-android.yml`** - Builds Android APK (debug and release versions)

---

## 🔄 Workflow Triggers

Both workflows trigger on:
- **Push** to `main` or `master` branches (only when relevant files change)
- **Pull Requests** to `main` or `master` branches
- **Manual trigger** via GitHub Actions UI (workflow_dispatch)

### Path Filters
- **Electron:** Only runs when files in `electron_app/` change
- **Android:** Only runs when files in `android_app/` change

This prevents unnecessary builds when you're only working on one app.

---

## 🖥️ Electron Desktop App Workflow

### Jobs

#### 1. Build Windows Executable
- **OS:** Windows Latest
- **Node.js:** Version 20
- **Package Manager:** Yarn
- **Output:** `.exe` files (portable + installer)

**Steps:**
1. Checkout code
2. Setup Node.js 20 with Yarn cache
3. Install dependencies (`yarn install`)
4. Build app (`yarn build`)
5. Package Windows executable (`yarn build:win`)
6. Extract version from `package.json`
7. Upload artifacts
8. Create GitHub Release (on push to main)

#### 2. Build Linux AppImage
- **OS:** Ubuntu Latest
- **Output:** `.AppImage` file

#### 3. Build macOS DMG
- **OS:** macOS Latest
- **Output:** `.dmg` file

### Artifacts Generated

All artifacts are stored for **30 days**:
- `ArmaReforgerMap-Windows-v1.0.0-Portable.exe`
- `ArmaReforgerMap-Windows-v1.0.0-Installer.exe`
- `ArmaReforgerMap-Linux-v1.0.0.AppImage`
- `ArmaReforgerMap-macOS-v1.0.0.dmg`

### Download Artifacts

1. Go to your GitHub repository
2. Click **Actions** tab
3. Select the workflow run
4. Scroll to **Artifacts** section
5. Download the file you need

---

## 📱 Android App Workflow

### Jobs

#### 1. Build Debug APK
- **OS:** Ubuntu Latest
- **JDK:** Version 17 (Temurin)
- **Build Tool:** Gradle
- **Output:** `app-debug.apk`

**Steps:**
1. Checkout code
2. Setup JDK 17
3. Grant execute permission to `gradlew`
4. Cache Gradle packages
5. Build debug APK (`./gradlew assembleDebug`)
6. Extract version from `build.gradle`
7. Upload debug APK

#### 2. Build Release APK
- **Trigger:** Only on push to main branch
- **Output:** `app-release-unsigned.apk`

**Note:** The release APK is unsigned. You'll need to sign it with your keystore for production use.

#### 3. Run Unit Tests
- Runs all unit tests
- Uploads test results as artifacts

#### 4. Run Lint Checks
- Checks code quality
- Uploads lint reports

### Artifacts Generated

- `ArmaReforgerMap-Android-Debug-v1.0.0.apk` (30 days)
- `ArmaReforgerMap-Android-Release-v1.0.0-unsigned.apk` (30 days)
- `test-results/` (7 days)
- `lint-results/` (7 days)

---

## 🚀 Using the Workflows

### First Time Setup

1. **Initialize Git** (if not already done):
   ```bash
   cd /app
   git init
   git add .
   git commit -m "Initial commit with Electron and Android apps"
   ```

2. **Create GitHub Repository:**
   - Go to https://github.com/new
   - Name: `arma-reforger-tactical-map`
   - Don't initialize with anything
   - Click "Create repository"

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/arma-reforger-tactical-map.git
   git branch -M main
   git push -u origin main
   ```

4. **Wait for Builds:**
   - GitHub Actions will automatically start
   - Go to Actions tab to watch progress
   - Builds take ~5-15 minutes

### Subsequent Updates

When you make changes:

```bash
# Make your changes in electron_app/ or android_app/

# Commit changes
git add .
git commit -m "Add new feature"
git push

# GitHub Actions will automatically build changed apps
```

---

## 📦 Releases

### Automatic Releases

When you push to the `main` branch:

**Electron:**
- Creates release tag: `v1.0.0`
- Attaches Windows, Linux, macOS builds
- Includes release notes

**Android:**
- Creates release tag: `android-v1.0.0`
- Attaches debug and unsigned release APKs
- Includes installation instructions

### Manual Release

To create a tagged release manually:

```bash
# For Electron
git tag v1.0.1
git push origin v1.0.1

# For Android
git tag android-v1.0.1
git push origin android-v1.0.1
```

---

## 🔧 Customization

### Change Version Number

**Electron:**
Edit `/app/electron_app/package.json`:
```json
{
  "version": "1.0.1"
}
```

**Android:**
Edit `/app/android_app/app/build.gradle`:
```gradle
versionCode 2
versionName "1.0.1"
```

### Add Build Secrets (for signing)

For signing Android APKs:

1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Add secrets:
   - `ANDROID_KEYSTORE_BASE64` - Base64 encoded keystore
   - `KEYSTORE_PASSWORD` - Keystore password
   - `KEY_ALIAS` - Key alias
   - `KEY_PASSWORD` - Key password

Then modify `build-android.yml` to use these secrets.

### Disable a Workflow

To temporarily disable a workflow:
1. Go to Actions tab
2. Select the workflow
3. Click "..." menu → Disable workflow

Or delete the `.yml` file.

---

## 📊 Build Status Badges

Add these to your `README.md`:

```markdown
![Electron Build](https://github.com/YOUR_USERNAME/arma-reforger-tactical-map/workflows/Build%20Electron%20Desktop%20App/badge.svg)
![Android Build](https://github.com/YOUR_USERNAME/arma-reforger-tactical-map/workflows/Build%20Android%20App/badge.svg)
```

---

## 🐛 Troubleshooting

### Electron Build Fails

**Issue:** Yarn install fails  
**Solution:** Delete `yarn.lock`, run `yarn install` locally, commit new lock file

**Issue:** TypeScript errors  
**Solution:** Run `yarn build` locally to catch errors before pushing

**Issue:** Native modules fail  
**Solution:** Ensure `better-sqlite3` is properly rebuilt for Electron

### Android Build Fails

**Issue:** Gradle wrapper not found  
**Solution:** Ensure `gradlew` has execute permissions: `chmod +x android_app/gradlew`

**Issue:** JDK version mismatch  
**Solution:** Workflow uses JDK 17, ensure `build.gradle` matches

**Issue:** Dependency resolution fails  
**Solution:** Update Gradle version in `gradle/wrapper/gradle-wrapper.properties`

**Issue:** Kotlin compiler error  
**Solution:** Check Kotlin version matches in `build.gradle`

### General Issues

**Issue:** Workflow doesn't trigger  
**Solution:** Check path filters match your changed files

**Issue:** Artifacts not uploaded  
**Solution:** Check artifact paths in workflow match actual build output

**Issue:** Out of storage  
**Solution:** GitHub provides 2GB storage. Delete old artifacts or reduce retention days

---

## 📁 File Structure

```
/app/
├── .github/
│   └── workflows/
│       ├── build-electron.yml    # ✅ Electron workflow
│       └── build-android.yml     # ✅ Android workflow
├── electron_app/
│   ├── package.json              # Version for Electron
│   └── ...
└── android_app/
    ├── app/
    │   └── build.gradle          # Version for Android
    ├── gradlew                   # ✅ Gradle wrapper (executable)
    └── ...
```

---

## ⚡ Quick Reference

### View Workflow Runs
```
https://github.com/YOUR_USERNAME/arma-reforger-tactical-map/actions
```

### Download Latest Artifacts
1. Go to Actions tab
2. Click latest successful run
3. Scroll to Artifacts section
4. Click to download

### Manually Trigger Build
1. Go to Actions tab
2. Select workflow (Electron or Android)
3. Click "Run workflow" button
4. Select branch
5. Click "Run workflow"

---

## 🎯 Next Steps

1. **Push to GitHub** - Workflows will run automatically
2. **Monitor builds** - Check Actions tab for progress
3. **Download artifacts** - Get built apps from completed workflows
4. **Test applications** - Install and test on target platforms
5. **Create releases** - Tag versions for public releases

---

## 📞 Support

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Electron Builder:** https://www.electron.build/
- **Android Gradle:** https://developer.android.com/build

---

**✅ Both workflows are ready to use. Simply push your code to GitHub and they'll build automatically!**
