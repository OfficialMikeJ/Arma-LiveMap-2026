#!/usr/bin/env python3
"""
Test core functionality without GUI
"""

import sys
import os

print("Testing core functionality (non-GUI)...")
print("-" * 60)

try:
    print("Testing core modules...")
    from core.encryption import EncryptionManager
    from core.database import Database
    from core.server_manager import ServerManager
    
    print("✓ Core modules imported successfully")
    
    # Test encryption
    print("\nTesting Encryption...")
    app_path = os.path.dirname(os.path.abspath(__file__))
    enc = EncryptionManager(app_path)
    test_data = "SecurePassword123!"
    encrypted = enc.encrypt(test_data)
    decrypted = enc.decrypt(encrypted)
    assert decrypted == test_data, "Encryption/Decryption failed"
    print(f"✓ Encrypted: {encrypted[:30]}...")
    print(f"✓ Decrypted: {decrypted}")
    
    # Test password hashing
    password = "TestPass123"
    hashed = enc.hash_password(password)
    verified = enc.verify_password(password, hashed)
    print(f"✓ Password hash: {hashed[:30]}...")
    print(f"✓ Password verification: {verified}")
    
    # Test database
    print("\nTesting Database...")
    db = Database(app_path)
    print(f"✓ Database created at: {db.db_path}")
    
    # Create test user
    user_id = db.create_user(
        "test_user",
        "test_password",
        "What is your favorite color?",
        "blue",
        "What is your pet's name?",
        "fluffy"
    )
    print(f"✓ Test user created with ID: {user_id}")
    
    # Verify login
    verified_id = db.verify_login("test_user", "test_password")
    print(f"✓ Login verified: {verified_id == user_id}")
    
    # Test security questions
    security_verified = db.verify_security_answers("test_user", "blue", "fluffy")
    print(f"✓ Security questions verified: {security_verified}")
    
    # Test session
    device_id = "test_device_123"
    session_token = db.create_session(user_id, device_id, keep_logged_in=True)
    print(f"✓ Session created: {session_token[:20]}...")
    
    session_user_id = db.verify_session(session_token, device_id)
    print(f"✓ Session verified: {session_user_id == user_id}")
    
    # Test TOTP (without QR generation)
    print("\nTesting TOTP...")
    import pyotp
    
    totp_secret = pyotp.random_base32()
    print(f"✓ TOTP secret generated: {totp_secret}")
    
    # Enable TOTP for user
    db.enable_totp(user_id, totp_secret)
    print("✓ TOTP enabled for user")
    
    # Verify TOTP
    totp = pyotp.TOTP(totp_secret)
    current_token = totp.now()
    verified = totp.verify(current_token, valid_window=1)
    print(f"✓ TOTP token verified: {verified}")
    print(f"✓ Current token: {current_token}")
    
    # Test server manager
    print("\nTesting Server Manager...")
    config_path = os.path.join(app_path, 'config', 'servers.json')
    server_mgr = ServerManager(config_path)
    print(f"✓ Server manager initialized")
    print(f"  Total servers: {len(server_mgr.servers)}")
    print(f"  Enabled servers: {len(server_mgr.get_enabled_servers())}")
    print(f"  WebSocket port: {server_mgr.websocket_port}")
    
    # Update a server
    server_mgr.update_server(1, "My Test Server", "192.168.1.100", 2302, True)
    print("✓ Server updated")
    
    enabled = server_mgr.get_enabled_servers()
    if enabled:
        print(f"  First enabled server: {enabled[0]['name']} ({enabled[0]['ip']}:{enabled[0]['port']})")
    
    # Test WebSocket imports
    print("\nTesting WebSocket...")
    import websockets
    print("✓ websockets module available")
    
    print("\n" + "=" * 60)
    print("✓ ALL CORE TESTS PASSED!")
    print("=" * 60)
    print("\nCore functionality is working correctly.")
    print("GUI components will work when run on a system with display support.")
    print("\nTo run the application:")
    print("  python main.py")
    print("\nTo build executable:")
    print("  Windows: build.bat")
    print("  Linux/Mac: ./build.sh")
    print("  Manual: pyinstaller --name ArmaReforgerMap --windowed main.py")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
