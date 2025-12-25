# Arma Reforger Live Interactive Map

## Desktop Application for Live Map Viewing and Enemy Marking

This is a Windows desktop application for Arma Reforger that provides:

- **Live Map View**: View real-time positions of friends on connected servers
- **Enemy Markers**: Mark enemy positions that are visible to all players on the server with minimal delay
- **Local Authentication**: Secure local account system with encrypted password storage
- **QR Code Authentication**: TOTP-based authentication using Google Authenticator or similar apps
- **Session Management**: "Keep me logged in for 60 days" functionality
- **Server Management**: Configure up to 6 servers with IP addresses and ports
- **Security Questions**: Password reset via security questions

## Features

### Authentication
- Local account creation with username and password
- Encrypted password storage using SHA-256 hashing
- Security questions for password recovery
- Optional TOTP/QR code authentication for enhanced security
- Persistent sessions (60-day login option)

### Map Functionality
- Interactive map viewer with zoom and pan
- Real-time marker placement (Enemy, Friendly, Objective, Other)
- WebSocket-based real-time synchronization
- Click to place markers, click again to remove
- Filter markers by type
- Clear your own markers

### Server Management
- Configure up to 6 servers
- Store server IP addresses and ports
- Enable/disable servers
- Switch between servers dynamically

## Installation

### Requirements
- Python 3.8 or higher
- PySide6
- websockets
- pyotp
- qrcode
- cryptography
- Pillow

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Building Executable

To build a standalone executable using PyInstaller:

```bash
pyinstaller --name "ArmaReforgerMap" --windowed --onefile --icon=assets/icon.ico main.py
```

For folder distribution (recommended for faster startup):

```bash
pyinstaller --name "ArmaReforgerMap" --windowed --icon=assets/icon.ico main.py
```

## GitHub Actions Build

Create `.github/workflows/build.yml`:

```yaml
name: Build Desktop App

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd desktop_app
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build with PyInstaller
      run: |
        cd desktop_app
        pyinstaller --name "ArmaReforgerMap" --windowed main.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: ArmaReforgerMap-Windows
        path: desktop_app/dist/
```

## Usage

### First Time Setup

1. Launch the application
2. Click "Create Account"
3. Enter username, password, and security questions
4. Login with your credentials

### Setting Up QR Code Authentication

1. Click "Settings" in the main window
2. Click "Enable QR Authentication"
3. Scan the QR code with Google Authenticator or similar app
4. Enter the 6-digit code to verify
5. Check "Keep me logged in for 60 days" on future logins

### Configuring Servers

1. Click "Settings" in the main window
2. Enable the server slots you want to use
3. Enter server name, IP address, and port
4. Click "Save Server Configuration"

### Using the Map

1. Select marker type from dropdown (Enemy, Friendly, Objective, Other)
2. Click on the map to place a marker
3. Click on an existing marker to remove it
4. Markers are synchronized in real-time with other users

## Data Storage

All data is stored locally in the `data/` folder:
- `arma_map.db`: SQLite database with users, sessions, and markers
- `.key`: Encryption key for password protection
- `.device_id`: Unique device identifier
- `.session`: Current session token

## Security

- Passwords are hashed using SHA-256
- Security answers are encrypted using Fernet encryption
- TOTP secrets are encrypted
- Session tokens are cryptographically secure
- All data stored locally (no internet transmission)

## Architecture

- **PySide6**: GUI framework
- **SQLite**: Local database
- **WebSockets**: Real-time communication
- **TOTP**: Time-based one-time passwords for QR authentication
- **Cryptography**: Fernet encryption for sensitive data

## License

MIT License
