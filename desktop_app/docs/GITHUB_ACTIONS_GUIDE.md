# GitHub Actions Build Guide

## How to Build .exe Using GitHub Actions

### Option 1: Automatic Build on Push (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Arma Reforger Map"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **GitHub Actions will automatically:**
   - Detect the push
   - Install Python 3.11
   - Install all dependencies
   - Build the .exe with PyInstaller
   - Create a portable package
   - Upload artifacts

3. **Download your .exe:**
   - Go to your GitHub repository
   - Click "Actions" tab
   - Click on the latest workflow run
   - Scroll to "Artifacts" section
   - Download `ArmaReforgerMap-Windows-Portable` or `ArmaReforgerMap-Windows-ZIP`

### Option 2: Manual Trigger

1. **Go to your GitHub repository**
2. **Click "Actions" tab**
3. **Select "Build Arma Reforger Map Desktop App"**
4. **Click "Run workflow" button**
5. **Select branch and click "Run workflow"**
6. **Wait for build to complete**
7. **Download from Artifacts**

### Option 3: Create a Release

For official releases with version tags:

```bash
# Tag your version
git tag v1.0.0
git push origin v1.0.0
```

This will:
- Build the application
- Create a GitHub Release
- Attach the ZIP file to the release
- Anyone can download from Releases page

### What Gets Built

The GitHub Actions workflow creates:

```
ArmaReforgerMap/
├── ArmaReforgerMap.exe          # Main executable
├── _internal/                   # Python runtime & dependencies
│   ├── PySide6/
│   ├── cryptography/
│   └── [all other dependencies]
├── config/
│   └── servers.json             # Server configuration
├── README.md                    # Documentation
└── QUICKSTART.md               # User guide
```

### Build Process Details

The workflow performs these steps:

1. **Checkout code** - Downloads your repository
2. **Setup Python 3.11** - Installs Python environment
3. **Install dependencies** - Installs all packages from requirements.txt
4. **Install PyInstaller** - Adds PyInstaller for .exe creation
5. **Build executable** - Creates `ArmaReforgerMap.exe` with `--onedir` flag
6. **Copy config files** - Includes server configuration
7. **Copy documentation** - Includes README and QUICKSTART
8. **Create ZIP** - Packages everything into a portable ZIP
9. **Upload artifacts** - Makes files downloadable

### Artifact Types

You'll get two downloadable artifacts:

1. **ArmaReforgerMap-Windows-Portable** (Folder)
   - Unzipped folder structure
   - Ready to run immediately
   - Best for development/testing

2. **ArmaReforgerMap-Windows-ZIP** (ZIP file)
   - Compressed portable package
   - Best for distribution
   - Users extract and run

### Build Configuration

The build uses these PyInstaller flags:

- `--name "ArmaReforgerMap"` - Names the executable
- `--windowed` - No console window (GUI only)
- `--onedir` - Creates folder with all dependencies (portable)

Alternative: For single-file .exe (slower startup):
```yaml
pyinstaller --name "ArmaReforgerMap" --windowed --onefile main.py
```

### Troubleshooting

#### Build fails with "Module not found"
- Check `requirements.txt` includes all dependencies
- Verify all import statements in your code

#### Build succeeds but .exe won't run
- Ensure PySide6 is in requirements.txt
- Check that config/ folder is copied to dist/

#### Can't find artifacts
- Wait for green checkmark (build complete)
- Check Actions tab → Latest run → Artifacts section
- Artifacts expire after 30 days (configurable)

#### Build takes too long
- Normal build time: 5-10 minutes
- Windows builds are slower than Linux
- PyInstaller analysis takes most time

### Local Build Alternative

If you prefer building locally instead of GitHub Actions:

**Windows:**
```batch
cd desktop_app
build.bat
```

**Linux/Mac:**
```bash
cd desktop_app
chmod +x build.sh
./build.sh
```

**Manual:**
```bash
cd desktop_app
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --name "ArmaReforgerMap" --windowed --onedir main.py
xcopy /E /I config dist\ArmaReforgerMap\config
```

### Distribution

Once built, distribute the entire `ArmaReforgerMap/` folder:

1. **ZIP it up:**
   ```bash
   # Windows PowerShell
   Compress-Archive -Path ArmaReforgerMap -DestinationPath ArmaReforgerMap-v1.0.0.zip
   ```

2. **Share the ZIP:**
   - GitHub Releases
   - Google Drive
   - Dropbox
   - Direct download link

3. **Users extract and run:**
   - No installation needed
   - Double-click `ArmaReforgerMap.exe`
   - First run creates `data/` folder

### Version Tagging

Recommended version format:

```bash
# Major release
git tag v1.0.0

# Minor update
git tag v1.1.0

# Patch/bugfix
git tag v1.0.1

# Push tag
git push origin v1.0.0
```

### File Sizes

Typical sizes:
- Folder (uncompressed): ~150-200 MB
- ZIP (compressed): ~50-80 MB
- Single-file .exe: ~100-120 MB

Size includes:
- Python runtime
- PySide6 (Qt) framework
- All dependencies
- Your application code

### Customization

To customize the build, edit `.github/workflows/build.yml`:

**Add an icon:**
```yaml
pyinstaller --name "ArmaReforgerMap" --windowed --onedir --icon=assets/icon.ico main.py
```

**Change version info:**
```yaml
pyinstaller --name "ArmaReforgerMap" --windowed --onedir --version-file=version.txt main.py
```

**Single-file build:**
```yaml
pyinstaller --name "ArmaReforgerMap" --windowed --onefile main.py
```

### Security Notes

- GitHub Actions is free for public repositories
- Private repositories have limited free minutes
- Secrets (API keys) can be added in repo settings
- Built .exe is not code-signed (Windows may show warning)

### Next Steps

1. ✅ Push code to GitHub
2. ✅ Enable Actions (automatic)
3. ✅ Wait for build (5-10 minutes)
4. ✅ Download artifacts
5. ✅ Test the .exe
6. ✅ Create release tag for v1.0.0
7. ✅ Share with users!

---

## Quick Reference

### Push and Build
```bash
git add .
git commit -m "Update application"
git push
# Wait 5-10 minutes
# Download from Actions → Artifacts
```

### Create Release
```bash
git tag v1.0.0
git push origin v1.0.0
# Wait 5-10 minutes
# Download from Releases page
```

### Local Build
```bash
cd desktop_app
build.bat  # Windows
# or
./build.sh  # Linux/Mac
```

---

**Your .exe will be fully portable and ready to distribute!** 🚀
