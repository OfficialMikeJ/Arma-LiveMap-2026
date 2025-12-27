@echo off
REM Quick Release Script for Windows
REM Usage: quick_release.bat 0.100.030 "Release description"

if "%1"=="" (
    echo Usage: quick_release.bat ^<version^> [description]
    echo Example: quick_release.bat 0.100.030 "Bug fixes and improvements"
    exit /b 1
)

set VERSION=%1
set DESCRIPTION=%~2
if "%DESCRIPTION%"=="" set DESCRIPTION=Version %VERSION% release

echo ======================================
echo Quick Release Script
echo ======================================
echo Version: %VERSION%
echo Description: %DESCRIPTION%
echo.

REM Step 1: Update version
echo [1/5] Updating version in code...
cd /d "%~dp0.."
python scripts\update_version.py %VERSION%
if errorlevel 1 (
    echo Error updating version
    exit /b 1
)

REM Step 2: Stage changes
echo [2/5] Staging changes...
git add .

REM Step 3: Commit
echo [3/5] Committing...
git commit -m "Release v%VERSION%" -m "%DESCRIPTION%"

REM Step 4: Create tag
echo [4/5] Creating tag...
git tag -a "v%VERSION%" -m "Version %VERSION%"

REM Step 5: Push
echo [5/5] Pushing to GitHub...
git push origin main
git push origin "v%VERSION%"

echo.
echo ======================================
echo Success! Release initiated
echo ======================================
echo.
echo Next steps:
echo 1. Go to GitHub Actions to monitor build
echo 2. Wait for build to complete (~5-10 minutes)
echo 3. Check Releases tab for new release
echo 4. Download and test the built executable
echo.
pause
