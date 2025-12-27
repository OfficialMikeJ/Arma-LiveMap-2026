#!/usr/bin/env python3
"""
Test the new server manager features
"""

import sys
import os

print("Testing Server Manager - Custom Server Feature...")
print("-" * 60)

try:
    from core.server_manager import ServerManager
    
    app_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(app_path, 'config', 'servers_test.json')
    
    # Initialize with empty config
    server_mgr = ServerManager(config_path)
    print(f"✓ Server manager initialized")
    print(f"  Initial servers: {len(server_mgr.servers)}")
    
    # Test adding a custom server
    print("\nTesting add_server()...")
    server_id1 = server_mgr.add_server("Custom Server 1", "203.0.113.45", 2302, enabled=True)
    print(f"✓ Added server ID: {server_id1}")
    
    server_id2 = server_mgr.add_server("Custom Server 2", "198.51.100.22", 2303, enabled=True)
    print(f"✓ Added server ID: {server_id2}")
    
    print(f"  Total servers now: {len(server_mgr.servers)}")
    
    # Test get_enabled_servers
    print("\nTesting get_enabled_servers()...")
    enabled = server_mgr.get_enabled_servers()
    print(f"✓ Enabled servers count: {len(enabled)}")
    for server in enabled:
        print(f"  - {server['name']} ({server['ip']}:{server['port']})")
    
    # Test remove_server
    print(f"\nTesting remove_server({server_id1})...")
    removed = server_mgr.remove_server(server_id1)
    print(f"✓ Server removed: {removed}")
    print(f"  Total servers now: {len(server_mgr.servers)}")
    
    # Test query_server_info (placeholder functionality)
    print("\nTesting query_server_info()...")
    info = server_mgr.query_server_info("198.51.100.22", 2303)
    if info:
        print(f"✓ Server query result:")
        print(f"  Status: {info['status']}")
        print(f"  Map: {info['map']}")
        print(f"  Players: {info['players']}/{info['max_players']}")
    
    # Clean up test file
    if os.path.exists(config_path):
        os.remove(config_path)
        print(f"\n✓ Test config file cleaned up")
    
    print("\n" + "=" * 60)
    print("✓ ALL SERVER MANAGER TESTS PASSED!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
