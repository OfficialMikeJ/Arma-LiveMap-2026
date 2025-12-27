import json
import os
import requests
from typing import List, Dict, Optional


class ServerManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.servers = []
        self.websocket_port = 8765
        self.load_config()
    
    def load_config(self):
        """Load server configuration from JSON"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.servers = config.get('servers', [])
                self.websocket_port = config.get('websocket_port', 8765)
    
    def save_config(self):
        """Save server configuration to JSON"""
        config = {
            'servers': self.servers,
            'websocket_port': self.websocket_port
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_enabled_servers(self) -> List[Dict]:
        """Get list of enabled servers"""
        return [s for s in self.servers if s.get('enabled', False)]
    
    def get_server_by_id(self, server_id: int) -> Optional[Dict]:
        """Get server by ID"""
        for server in self.servers:
            if server['id'] == server_id:
                return server
        return None
    
    def update_server(self, server_id: int, name: str, ip: str, port: int, enabled: bool):
        """Update server configuration"""
        for server in self.servers:
            if server['id'] == server_id:
                server['name'] = name
                server['ip'] = ip
                server['port'] = port
                server['enabled'] = enabled
                break
        self.save_config()
    
    def add_server(self, name: str, ip: str, port: int, enabled: bool = True) -> int:
        """Add a new server to the list"""
        # Find next available ID
        existing_ids = [s['id'] for s in self.servers]
        next_id = max(existing_ids) + 1 if existing_ids else 1
        
        new_server = {
            'id': next_id,
            'name': name,
            'ip': ip,
            'port': port,
            'enabled': enabled
        }
        
        self.servers.append(new_server)
        self.save_config()
        return next_id
    
    def remove_server(self, server_id: int) -> bool:
        """Remove a server from the list"""
        for i, server in enumerate(self.servers):
            if server['id'] == server_id:
                self.servers.pop(i)
                self.save_config()
                return True
        return False
    
    def query_server_info(self, ip: str, port: int) -> Optional[Dict]:
        """Query server for map and player information
        Note: This is a placeholder - actual implementation depends on Arma Reforger server API
        """
        try:
            # Placeholder for actual server query
            # In real implementation, this would connect to Arma Reforger server
            # and retrieve current map, player positions, etc.
            
            return {
                'status': 'online',
                'map': 'Everon',
                'players': 0,
                'max_players': 64
            }
        except Exception as e:
            print(f"Error querying server {ip}:{port} - {e}")
            return None
