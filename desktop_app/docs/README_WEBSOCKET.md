# WebSocket Server Guide

## Overview

The Arma Reforger Live Map uses WebSocket technology for real-time communication between clients. This enables instant marker updates, player position tracking, and chat messages across all connected users.

## Starting the WebSocket Server

### Method 1: Standalone Server (Recommended)

Run the WebSocket server as a standalone process:

```bash
# Default settings (localhost:8765)
python run_websocket_server.py

# Custom host and port
python run_websocket_server.py --host 0.0.0.0 --port 9000
```

### Method 2: Background Process

On Linux/Mac:
```bash
nohup python run_websocket_server.py &
```

On Windows:
```cmd
start /B python run_websocket_server.py
```

## Server Configuration

The WebSocket server configuration is stored in `config/servers.json`:

```json
{
  "servers": [...],
  "websocket_port": 8765
}
```

## Features

### 1. Real-Time Marker Synchronization
- Markers placed by any user are instantly visible to all connected users
- Marker removal is synchronized across all clients
- Persistent marker storage on the server

### 2. Player Position Updates
- Live tracking of player positions on the map
- Position data stored per user
- Automatic position sync when new clients connect

### 3. Chat Messages (Future Feature)
- Real-time chat between connected users
- Message broadcasting to all clients

### 4. Connection Management
- Automatic client registration/unregistration
- Ping/pong for connection health monitoring
- Graceful handling of disconnections

## Message Protocol

### Client → Server Messages

#### Add Marker
```json
{
  "type": "marker_add",
  "marker": {
    "type": "enemy",
    "x": 500.5,
    "y": 300.2,
    "user_id": 1,
    "description": "Enemy spotted",
    "timestamp": "2026-01-01T12:00:00"
  }
}
```

#### Remove Marker
```json
{
  "type": "marker_remove",
  "marker_id": "1_1704110400"
}
```

#### Position Update
```json
{
  "type": "position_update",
  "player": {
    "user_id": 1,
    "username": "Player1",
    "x": 450.0,
    "y": 320.0,
    "team": "blue",
    "timestamp": "2026-01-01T12:00:00"
  }
}
```

#### Ping
```json
{
  "type": "ping",
  "timestamp": "2026-01-01T12:00:00"
}
```

### Server → Client Messages

#### Marker Added
```json
{
  "type": "marker_added",
  "marker": {
    "id": "1_1704110400",
    "type": "enemy",
    "x": 500.5,
    "y": 300.2,
    "user_id": 1,
    "description": "Enemy spotted",
    "timestamp": "2026-01-01T12:00:00"
  }
}
```

#### Marker Removed
```json
{
  "type": "marker_removed",
  "marker_id": "1_1704110400"
}
```

#### Markers Sync (on connect)
```json
{
  "type": "markers_sync",
  "markers": [
    {"id": "1_1704110400", "type": "enemy", ...},
    {"id": "2_1704110500", "type": "friendly", ...}
  ]
}
```

#### Positions Sync (on connect)
```json
{
  "type": "positions_sync",
  "positions": [
    {"user_id": 1, "username": "Player1", "x": 450, "y": 320, ...}
  ]
}
```

#### Pong (response to ping)
```json
{
  "type": "pong",
  "timestamp": "2026-01-01T12:00:00"
}
```

## Arma Server Integration

The `ArmaServerConnector` class provides an interface for connecting to actual Arma Reforger game servers:

```python
from core.arma_server_connector import ArmaServerConnector

# Create connector
connector = ArmaServerConnector(ip="192.168.1.100", port=2302)

# Connect
await connector.connect()

# Get server info
info = await connector.get_server_info()
print(f"Map: {info['map']}, Players: {info['player_count']}")

# Get player positions
positions = await connector.get_player_positions()
for pos in positions:
    print(f"{pos['username']}: ({pos['x']}, {pos['y']})")

# Disconnect
await connector.disconnect()
```

**Note:** The current implementation is simulated since Arma Reforger's server query protocol is not publicly documented. In a production environment, you would implement the actual protocol based on Bohemia Interactive's documentation.

## Testing

### Test WebSocket Server

```bash
python test_core.py
```

This will test:
- WebSocket module availability
- Server manager configuration
- Core functionality

### Manual Testing

1. Start the WebSocket server:
   ```bash
   python run_websocket_server.py
   ```

2. Run the desktop app:
   ```bash
   python main.py
   ```

3. Open multiple instances of the app and verify:
   - Markers appear on all clients
   - Marker removal syncs across clients
   - Connection status shows "Connected"

## Troubleshooting

### Server Won't Start
- Check if port 8765 is already in use
- Try a different port: `python run_websocket_server.py --port 9000`
- Check firewall settings

### Client Can't Connect
- Verify the WebSocket server is running
- Check the port number in `config/servers.json`
- Ensure the host/port matches the server configuration

### Markers Not Syncing
- Check the console for WebSocket errors
- Verify the client shows "Connected" status
- Check server logs for error messages

## Production Deployment

### Using systemd (Linux)

Create `/etc/systemd/system/arma-websocket.service`:

```ini
[Unit]
Description=Arma Reforger Live Map WebSocket Server
After=network.target

[Service]
Type=simple
User=arma
WorkingDirectory=/path/to/desktop_app
ExecStart=/usr/bin/python3 run_websocket_server.py --host 0.0.0.0 --port 8765
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable arma-websocket
sudo systemctl start arma-websocket
sudo systemctl status arma-websocket
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8765

CMD ["python", "run_websocket_server.py", "--host", "0.0.0.0"]
```

Build and run:
```bash
docker build -t arma-websocket .
docker run -d -p 8765:8765 --name arma-ws arma-websocket
```

## Performance Considerations

- The server can handle multiple simultaneous connections
- Marker data is stored in memory for fast access
- Position updates are broadcasted without storage by default
- For large deployments (100+ users), consider using Redis for state management

## Security Considerations

- The current implementation does not include authentication at the WebSocket level
- All authenticated users (via the desktop app) can connect
- For public deployments, implement token-based WebSocket authentication
- Use WSS (WebSocket Secure) for encrypted connections

## Future Enhancements

- [ ] Token-based WebSocket authentication
- [ ] WSS (secure WebSocket) support
- [ ] Redis integration for distributed deployments
- [ ] Actual Arma Reforger server protocol implementation
- [ ] Voice chat integration
- [ ] File/image sharing
- [ ] Admin commands via WebSocket
