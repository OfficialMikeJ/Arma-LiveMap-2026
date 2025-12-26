@echo off
REM Quick Push Script for Arma Reforger Map (Windows)

echo ================================================
echo   Arma Reforger Map - GitHub Push Script
echo ================================================
echo.

REM Check if we're in the right directory
if not exist "desktop_app\main.py" (
    echo Error: Run this script from the repository root
    echo   cd /path/to/repo
    echo   push_to_github.bat
    exit /b 1
)

echo [OK] Correct directory
echo.

REM Check if .github exists at root
if not exist ".github\workflows\build.yml" (
    echo Error: .github\workflows\build.yml not found at root
    echo   The workflow file must be at repository root!
    exit /b 1
)

echo [OK] GitHub Actions workflow found at root
echo.

REM Initialize git if needed
if not exist ".git" (
    echo Initializing git repository...
    git init
    git branch -M main
    echo [OK] Git initialized
    echo.
)

REM Show what will be added
echo Files to be committed:
echo   - .github/workflows/build.yml (GitHub Actions)
echo   - desktop_app/ (Your application)
echo   - Documentation files
echo.

REM Ask for GitHub repository URL
set /p REPO_URL="Enter your GitHub repository URL: "

if "%REPO_URL%"=="" (
    echo Error: Repository URL is required
    exit /b 1
)

echo.
echo Setting up remote...
git remote remove origin 2>nul
git remote add origin "%REPO_URL%"

echo [OK] Remote set to: %REPO_URL%
echo.

REM Add files
echo Adding files to git...
git add .github/
git add desktop_app/
git add GITHUB_ACTIONS_FIX.md
git add README.md 2>nul
git add .gitignore 2>nul

echo [OK] Files added
echo.

REM Commit
echo Creating commit...
git commit -m "Add Arma Reforger Live Interactive Map with GitHub Actions"

echo [OK] Commit created
echo.

REM Push
echo Pushing to GitHub...
echo.
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo   SUCCESS!
    echo ================================================
    echo.
    echo Your code is now on GitHub!
    echo.
    echo Next steps:
    echo   1. Go to your GitHub repository
    echo   2. Click the Actions tab
    echo   3. Wait 5-10 minutes for the build
    echo   4. Download artifacts when complete
    echo.
) else (
    echo.
    echo ================================================
    echo   PUSH FAILED
    echo ================================================
    echo.
    echo Common issues:
    echo   - Authentication: Use Personal Access Token
    echo   - Permissions: Check write access
    echo   - Remote URL: Verify repository URL
    echo.
)

pause
