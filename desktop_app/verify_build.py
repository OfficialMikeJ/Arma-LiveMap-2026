#!/usr/bin/env python3
"""
Pre-build verification script
Checks that everything is ready for PyInstaller build
"""

import os
import sys
import json

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - MISSING!")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - MISSING!")
        return False

def main():
    print("=" * 70)
    print("Arma Reforger Map - Pre-Build Verification")
    print("=" * 70)
    print()
    
    all_ok = True
    
    # Check core structure
    print("Checking Project Structure...")
    print("-" * 70)
    all_ok &= check_file("main.py", "Main application entry point")
    all_ok &= check_file("requirements.txt", "Dependencies file")
    all_ok &= check_directory("core", "Core modules directory")
    all_ok &= check_directory("gui", "GUI modules directory")
    all_ok &= check_directory("map", "Map modules directory")
    all_ok &= check_directory("config", "Configuration directory")
    print()
    
    # Check core modules
    print("Checking Core Modules...")
    print("-" * 70)
    all_ok &= check_file("core/__init__.py", "Core package marker")
    all_ok &= check_file("core/auth.py", "Authentication manager")
    all_ok &= check_file("core/database.py", "Database operations")
    all_ok &= check_file("core/encryption.py", "Encryption utilities")
    all_ok &= check_file("core/websocket_server.py", "WebSocket server")
    all_ok &= check_file("core/server_manager.py", "Server manager")
    print()
    
    # Check GUI modules
    print("Checking GUI Modules...")
    print("-" * 70)
    all_ok &= check_file("gui/__init__.py", "GUI package marker")
    all_ok &= check_file("gui/styles.py", "Theme styles")
    all_ok &= check_file("gui/login_window.py", "Login window")
    all_ok &= check_file("gui/main_window.py", "Main window")
    all_ok &= check_file("gui/settings_window.py", "Settings window")
    print()
    
    # Check map modules
    print("Checking Map Modules...")
    print("-" * 70)
    all_ok &= check_file("map/__init__.py", "Map package marker")
    all_ok &= check_file("map/map_viewer.py", "Map viewer")
    print()
    
    # Check configuration
    print("Checking Configuration...")
    print("-" * 70)
    all_ok &= check_file("config/servers.json", "Server configuration")
    
    # Validate servers.json
    try:
        with open("config/servers.json", 'r') as f:
            config = json.load(f)
            if 'servers' in config and len(config['servers']) == 6:
                print("✓ Server configuration valid (6 server slots)")
            else:
                print("✗ Server configuration invalid")
                all_ok = False
    except Exception as e:
        print(f"✗ Error reading server configuration: {e}")
        all_ok = False
    print()
    
    # Check build files
    print("Checking Build Files...")
    print("-" * 70)
    all_ok &= check_file("build.bat", "Windows build script")
    all_ok &= check_file("build.sh", "Linux/Mac build script")
    all_ok &= check_file("ArmaReforgerMap.spec", "PyInstaller spec file")
    print()
    
    # Check documentation
    print("Checking Documentation...")
    print("-" * 70)
    all_ok &= check_file("README.md", "Main documentation")
    all_ok &= check_file("QUICKSTART.md", "Quick start guide")
    all_ok &= check_file("PROJECT_SUMMARY.md", "Project summary")
    all_ok &= check_file("STRUCTURE.md", "Structure documentation")
    print()
    
    # Check GitHub Actions
    print("Checking GitHub Actions...")
    print("-" * 70)
    all_ok &= check_file(".github/workflows/build.yml", "GitHub Actions workflow")
    print()
    
    # Check Python version
    print("Checking Python Environment...")
    print("-" * 70)
    print(f"✓ Python version: {sys.version}")
    
    # Try importing key dependencies
    print("\nChecking Key Dependencies...")
    print("-" * 70)
    
    dependencies = [
        ("PySide6", "PySide6 GUI framework"),
        ("websockets", "WebSocket library"),
        ("pyotp", "TOTP authentication"),
        ("qrcode", "QR code generation"),
        ("cryptography", "Encryption library"),
        ("PIL", "Pillow image library"),
    ]
    
    for module_name, description in dependencies:
        try:
            __import__(module_name)
            print(f"✓ {description}")
        except ImportError:
            print(f"✗ {description} - NOT INSTALLED!")
            all_ok = False
    
    print()
    print("=" * 70)
    
    if all_ok:
        print("✅ ALL CHECKS PASSED!")
        print("=" * 70)
        print("\nYour project is ready to build!")
        print("\nNext steps:")
        print("  1. Run core tests: python test_core.py")
        print("  2. Build executable:")
        print("     - Windows: build.bat")
        print("     - Linux/Mac: ./build.sh")
        print("     - Manual: pyinstaller --name ArmaReforgerMap --windowed main.py")
        print("\n  3. Find executable in: dist/ArmaReforgerMap/")
        return 0
    else:
        print("❌ SOME CHECKS FAILED!")
        print("=" * 70)
        print("\nPlease fix the issues above before building.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
