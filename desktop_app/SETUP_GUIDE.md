# Complete Setup & Build Instructions

## 🎯 Goal
Build a portable Windows .exe file for the Arma Reforger Live Interactive Map application using GitHub Actions.

---

## 📋 Prerequisites

- GitHub account (free)
- Git installed on your computer
- The desktop_app folder from this project

---

## 🚀 Step-by-Step Setup

### Step 1: Create GitHub Repository

1. Go to https://github.com
2. Click the **"+"** icon → **"New repository"**
3. Repository details:
   - Name: `arma-reforger-map` (or your choice)
   - Description: "Live Interactive Map for Arma Reforger"
   - Visibility: Public (for free Actions) or Private
   - **Do NOT** initialize with README, .gitignore, or license
4. Click **"Create repository"**

### Step 2: Prepare Your Local Files

Open terminal/command prompt in the desktop_app folder:

```bash
cd /path/to/desktop_app
```

Initialize git:
```bash
git init
git branch -M main
```

### Step 3: Create .gitignore (Important!)

Create a file named `.gitignore` in the desktop_app folder:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Runtime data
data/
*.db
.key
.device_id
.session

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

### Step 4: Add Files to Git

```bash
git add .
git commit -m "Initial commit - Arma Reforger Live Interactive Map"
```

### Step 5: Connect to GitHub

Replace `YOUR_USERNAME` and `YOUR_REPO` with your actual values:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

You may need to authenticate:
- Use GitHub username and **Personal Access Token** (not password)
- Or use SSH keys if configured

### Step 6: Verify GitHub Actions

1. Go to your GitHub repository
2. Click **"Actions"** tab
3. You should see **"Build Arma Reforger Map Desktop App"** workflow
4. It should start running automatically after your push
5. Wait 5-10 minutes for the build to complete

### Step 7: Download Your .exe

Once the workflow shows a green checkmark:

1. Click on the workflow run name
2. Scroll down to **"Artifacts"** section
3. Download **"ArmaReforgerMap-Windows-ZIP"**
4. Extract the ZIP file
5. Inside you'll find `ArmaReforgerMap.exe`

---

## 🔄 Updating and Rebuilding

When you make changes to the code:

```bash
# Make your changes to files
# Then commit and push:

git add .
git commit -m "Description of your changes"
git push
```

GitHub Actions will automatically rebuild the .exe!

---

## 📦 Creating Official Releases

For version releases that appear on your repo's Releases page:

```bash
# Tag your version
git tag v1.0.0
git push origin v1.0.0
```

This will:
- Trigger a build
- Create a GitHub Release
- Automatically attach the .exe ZIP to the release
- Make it easy for users to download

---

## 🛠️ Local Build (Alternative Method)

If you prefer building locally without GitHub Actions:

### Windows:
```batch
cd desktop_app
build.bat
```

The .exe will be in: `desktop_app/dist/ArmaReforgerMap/`

### Linux/Mac:
```bash
cd desktop_app
chmod +x build.sh
./build.sh
```

---

## 📊 What Gets Built

```
ArmaReforgerMap-Windows-Portable.zip
└── ArmaReforgerMap/
    ├── ArmaReforgerMap.exe       ← Main executable
    ├── _internal/                 ← Python & dependencies
    │   ├── PySide6/
    │   ├── cryptography/
    │   └── [other libs]
    ├── config/
    │   └── servers.json
    ├── README.md
    └── QUICKSTART.md
```

**Total size:** ~50-80 MB (compressed), ~150-200 MB (extracted)

---

## ✅ Testing Your .exe

1. Extract the ZIP file to any folder
2. Double-click `ArmaReforgerMap.exe`
3. You should see the login window
4. Create an account and test features

---

## 🔍 Troubleshooting

### "Actions tab not visible"
- Check if Actions are enabled in Settings → Actions → General
- For private repos, check if you have Actions minutes remaining

### "Build failed"
- Click on the failed workflow
- Check the error logs
- Common issues:
  - Missing dependency in requirements.txt
  - Syntax error in Python code
  - Path issues in build.yml

### "Can't push to GitHub"
- Verify remote URL: `git remote -v`
- Check authentication (use Personal Access Token)
- For SSH: Ensure SSH key is added to GitHub

### ".exe won't run"
- Windows may show "Unknown Publisher" warning (click "More Info" → "Run anyway")
- Check antivirus didn't block it
- Ensure all files in folder (don't move .exe alone)

### "Build succeeds but can't find artifact"
- Artifacts expire after 30 days
- Re-run the workflow to generate new artifacts
- Check you're looking at the correct workflow run

---

## 📝 File Checklist

Ensure these files exist in your desktop_app folder before pushing:

```
✓ main.py
✓ requirements.txt
✓ .github/workflows/build.yml
✓ core/ (all Python files)
✓ gui/ (all Python files)
✓ map/ (all Python files)
✓ config/servers.json
✓ build.bat
✓ build.sh
✓ README.md
✓ QUICKSTART.md
```

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Initial setup | `git init && git add . && git commit -m "Initial"` |
| Push to GitHub | `git push -u origin main` |
| Update code | `git add . && git commit -m "Update" && git push` |
| Create release | `git tag v1.0.0 && git push origin v1.0.0` |
| Local build | `build.bat` (Windows) or `./build.sh` (Linux/Mac) |

---

## 📞 Need Help?

1. Check the build logs in GitHub Actions
2. Review QUICKSTART.md for usage help
3. Run `python test_core.py` to verify code works
4. Run `python verify_build.py` to check file structure

---

## 🎉 Success Criteria

You've succeeded when:
- ✅ Code is on GitHub
- ✅ Green checkmark in Actions tab
- ✅ Artifacts available for download
- ✅ .exe runs without errors
- ✅ Can create account and see login window
- ✅ Map displays correctly

**Your portable .exe is ready to distribute!** 🚀

---

## 📚 Additional Resources

- **GITHUB_ACTIONS_GUIDE.md** - Detailed Actions documentation
- **QUICKSTART.md** - User guide for the application
- **README.md** - Technical documentation
- **PROJECT_SUMMARY.md** - Feature overview

---

## 🔐 Security Notes

- GitHub Actions builds are reproducible
- All dependencies come from PyPI (pip)
- No external binaries or executables
- Source code is visible (if public repo)
- .exe is not code-signed (Windows warning is normal)

To add code signing, you'd need a certificate ($200-400/year).

---

**You're all set! Follow the steps above to get your .exe file.** ✨
