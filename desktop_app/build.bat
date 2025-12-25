# Build script for Windows
# Run this to build the executable

@echo off
echo Building Arma Reforger Map Desktop Application...
echo.

echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Building executable...
pyinstaller --name "ArmaReforgerMap" --windowed --onedir main.py

echo.
echo Copying config files...
xcopy /E /I config dist\ArmaReforgerMap\config

echo.
echo Build complete!
echo Executable location: dist\ArmaReforgerMap\ArmaReforgerMap.exe
echo.
pause
