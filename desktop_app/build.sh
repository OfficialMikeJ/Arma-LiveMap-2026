#!/bin/bash
# Build script for Linux/Mac
# Run this to build the executable

echo "Building Arma Reforger Map Desktop Application..."
echo ""

echo "Installing dependencies..."
pip install -r requirements.txt
pip install pyinstaller

echo ""
echo "Building executable..."
pyinstaller --name "ArmaReforgerMap" --windowed --onedir main.py

echo ""
echo "Copying config files..."
cp -r config dist/ArmaReforgerMap/

echo ""
echo "Build complete!"
echo "Executable location: dist/ArmaReforgerMap/ArmaReforgerMap"
echo ""
