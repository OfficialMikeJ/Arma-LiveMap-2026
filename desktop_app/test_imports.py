#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

import sys
import os

print("Testing imports for Arma Reforger Map application...")
print("-" * 60)

try:
    print("✓ Python version:", sys.version)
    print()
    
    print("Testing PySide6...")
    from PySide6.QtWidgets import QApplication, QMainWindow
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtGui import QPixmap
    print("✓ PySide6 imports successful")
    
    print("\nTesting websockets...")
    import websockets
    print("✓ websockets imports successful")
    
    print("\nTesting pyotp...")
    import pyotp
    print("✓ pyotp imports successful")
    
    print("\nTesting qrcode...")
    import qrcode
    print("✓ qrcode imports successful")
    
    print("\nTesting cryptography...")
    from cryptography.fernet import Fernet
    print("✓ cryptography imports successful")
    
    print("\nTesting Pillow...")
    from PIL import Image
    print("✓ Pillow imports successful")
    
    print("\nTesting application modules...")
    from core.encryption import EncryptionManager
    print("✓ core.encryption imported")
    
    from core.database import Database
    print("✓ core.database imported")
    
    from core.auth import AuthManager
    print("✓ core.auth imported")
    
    from core.websocket_server import WebSocketServer
    print("✓ core.websocket_server imported")
    
    from core.server_manager import ServerManager
    print("✓ core.server_manager imported")
    
    from gui.styles import DARK_THEME
    print("✓ gui.styles imported")
    
    from gui.login_window import LoginWindow
    print("✓ gui.login_window imported")
    
    from gui.settings_window import SettingsWindow
    print("✓ gui.settings_window imported")
    
    from gui.main_window import MainWindow
    print("✓ gui.main_window imported")
    
    from map.map_viewer import MapViewer, MapMarker
    print("✓ map.map_viewer imported")
    
    print("\n" + "=" * 60)
    print("✓ All imports successful!")
    print("=" * 60)
    
    print("\nTesting basic functionality...")
    
    # Test encryption
    app_path = os.path.dirname(os.path.abspath(__file__))
    enc = EncryptionManager(app_path)
    test_data = "test_password_123"
    encrypted = enc.encrypt(test_data)
    decrypted = enc.decrypt(encrypted)
    assert decrypted == test_data, "Encryption/Decryption failed"
    print("✓ Encryption/Decryption working")
    
    # Test database
    db = Database(app_path)
    print("✓ Database initialized")
    
    # Test auth manager
    auth = AuthManager(db)
    print("✓ Auth manager initialized")
    
    # Test server manager
    config_path = os.path.join(app_path, 'config', 'servers.json')
    server_mgr = ServerManager(config_path)
    print("✓ Server manager initialized")
    print(f"  Servers configured: {len(server_mgr.servers)}")
    print(f"  Enabled servers: {len(server_mgr.get_enabled_servers())}")
    
    # Test TOTP
    secret = auth.generate_totp_secret()
    print(f"✓ TOTP secret generated: {secret[:10]}...")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nThe application is ready to be built with PyInstaller.")
    print("Run: python main.py (to test with GUI)")
    print("Or: ./build.bat (Windows) or ./build.sh (Linux/Mac)")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
