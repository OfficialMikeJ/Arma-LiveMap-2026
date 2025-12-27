# Arma Reforger Live Interactive Map - Quick Start Guide

## Overview
A Windows desktop application providing real-time map viewing and enemy marking for Arma Reforger servers.

## Key Features
✓ **Live Map Viewing**: Real-time map with player positions
✓ **Enemy Markers**: Place and remove markers visible to all users
✓ **Secure Login**: Local encrypted account system
✓ **QR Code Auth**: TOTP authentication using Google Authenticator
✓ **60-Day Sessions**: Stay logged in option
✓ **Multi-Server Support**: Configure up to 6 servers
✓ **Password Recovery**: Security question-based password reset

## Quick Start

### 1. First Run
When you launch the application for the first time:

1. Click **"Create Account"**
2. Enter:
   - Username
   - Password (minimum 4 characters)
   - Confirm password
   - Answer 2 security questions
3. Click **OK**
4. Login with your new credentials

### 2. Configure Servers
After logging in:

1. Click **"Settings"** in the toolbar
2. Under "Server Configuration":
   - Check the box for Server 1
   - Enter server name (e.g., "My Arma Server")
   - Enter IP address (e.g., "127.0.0.1")
   - Enter port (e.g., "2001")
3. Click **"Save Server Configuration"**

### 3. Setup QR Code Authentication (Optional)
For enhanced security with "Keep me logged in":

1. Click **"Settings"**
2. Click **"Enable QR Authentication"**
3. Scan QR code with Google Authenticator app
4. Enter the 6-digit code
5. Click **OK**

Now you can use QR codes to login and stay logged in for 60 days!

### 4. Using the Map

#### Placing Markers
1. Select marker type from dropdown:
   - **Enemy**: Red markers for hostiles
   - **Friendly**: Blue markers for allies
   - **Objective**: Yellow markers for targets
   - **Other**: Gray markers for misc
2. Click anywhere on the map to place a marker
3. Markers appear instantly for all connected users

#### Removing Markers
- Click on any marker to remove it
- Use **"Clear My Markers"** to remove all your markers at once

#### Switching Servers
- Use the **Server** dropdown to switch between configured servers
- Each server maintains its own set of markers

## Building the Executable

### Windows
```batch
build.bat
```

Or manually:
```batch
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --name "ArmaReforgerMap" --windowed --onedir main.py
```

### Linux/Mac
```bash
chmod +x build.sh
./build.sh
```

The executable will be in: `dist/ArmaReforgerMap/`

## GitHub Actions Automatic Build

The project includes `.github/workflows/build.yml` for automatic builds:

1. Push code to GitHub
2. GitHub Actions automatically builds Windows executable
3. Download from Actions artifacts tab

For release builds:
```bash
git tag v1.0.0
git push origin v1.0.0
```

## File Structure
```
ArmaReforgerMap/
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── build.bat / build.sh      # Build scripts
├── config/
│   └── servers.json          # Server configuration
├── core/
│   ├── auth.py               # Authentication
│   ├── database.py           # SQLite operations
│   ├── encryption.py         # Encryption utilities
│   ├── websocket_server.py   # Real-time communication
│   └── server_manager.py     # Server management
├── gui/
│   ├── login_window.py       # Login interface
│   ├── main_window.py        # Main map window
│   ├── settings_window.py    # Settings interface
│   └── styles.py             # Dark theme styling
└── map/
    └── map_viewer.py         # Interactive map viewer
```

## Data Storage
All data is stored locally in `data/` folder:
- `arma_map.db` - User accounts, sessions, markers
- `.key` - Encryption key
- `.device_id` - Unique device identifier
- `.session` - Current session token

## Troubleshooting

### "Cannot connect to server"
- Check that the WebSocket server is running (automatic on startup)
- Verify server IP and port are correct in Settings
- Check firewall settings

### "Invalid username or password"
- Use "Forgot Password?" link
- Answer security questions to reset password

### QR Code not working
1. Ensure time is synchronized on your computer
2. Try entering the manual entry key instead
3. Use "Disable QR Authentication" and set up again

### Application won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version is 3.8 or higher
- Run `python test_core.py` to verify core functionality

## Security Notes
- All data stored locally (never transmitted over internet)
- Passwords hashed with SHA-256
- Security answers encrypted with Fernet
- TOTP secrets encrypted
- Session tokens cryptographically secure

## System Requirements
- **OS**: Windows 10/11, Linux, or macOS
- **Python**: 3.8 or higher (for development)
- **RAM**: 256MB minimum
- **Storage**: 50MB for application + data

## Support
For issues or questions:
1. Check this guide first
2. Run `python test_core.py` to verify installation
3. Review error messages in console

## Advanced Configuration

### Customizing WebSocket Port
Edit `config/servers.json`:
```json
{
  "websocket_port": 8765
}
```

### Multiple Instances
Each copy of the application in a different folder is independent with its own:
- User database
- Session storage
- Server configuration

### Server Array Configuration
You can directly edit `config/servers.json`:
```json
{
  "servers": [
    {
      "id": 1,
      "name": "Main Server",
      "ip": "192.168.1.100",
      "port": 2302,
      "enabled": true
    }
  ]
}
```

## Development

### Running from Source
```bash
cd desktop_app
pip install -r requirements.txt
python main.py
```

### Testing
```bash
python test_core.py    # Test core functionality
python main.py         # Full application test
```

### Custom Modifications
- **Change theme colors**: Edit `gui/styles.py`
- **Add map images**: Place in `assets/maps/` and use `map_viewer.load_map_image()`
- **Custom marker types**: Modify `map/map_viewer.py`

## License
MIT License - Feel free to modify and distribute.
