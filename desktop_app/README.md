# Arma Reforger Live Interactive Map

**Current Version:** 0.096.014  
**Next Release:** 0.099.021 (Coming 2026)

## Desktop Application for Live Map Viewing and Enemy Marking

This is a Windows desktop application for Arma Reforger that provides real-time tactical map viewing and coordination capabilities for teams and friends.

---

## 📦 Version Information

### Current Version: 0.096.014

**Release Date:** December 2025  
**Status:** Stable

#### Features in 0.096.014:
- ✅ Live Map View with real-time synchronization
- ✅ Enemy Markers (Enemy, Friendly, Objective, Other)
- ✅ Local Authentication with encrypted storage
- ✅ QR Code/TOTP Authentication (Google Authenticator)
- ✅ Session Management ("Keep me logged in for 60 days")
- ✅ Server Management (up to 6 servers)
- ✅ Security Questions for password recovery
- ✅ WebSocket-based real-time marker synchronization
- ✅ Basic map interaction (click to place/remove)

### Next Version: 0.099.021 (Planned for 2026)

**Status:** In Development

#### New Features in 0.099.021:
- 🆕 **Map Zoom Controls**: +/- buttons and Ctrl+Mouse Wheel zoom
- 🆕 **Enhanced Map Scrolling**: Improved navigation across entire map area
- 🆕 **Vanilla Arma Reforger Markers**: Support for all official marker types
  - Attack, Defend, Pickup, Drop, Meet
  - Infantry, Armor, Air, Naval
  - Different shapes (circle, square, diamond, triangle, arrow, star)
- 🆕 **Advanced Filter System**: Show/hide markers by type
  - Individual toggle for each marker type
  - Select All/None quick actions
  - Real-time filter application
- 🆕 **Feedback System**: Built-in feedback submission
  - Bug reports
  - Feature requests
  - Direct Discord community link
  - Local storage (admin dashboard integration coming later)

---

## 🎯 Core Features

### Authentication & Security
- Local account creation with username and password
- SHA-256 password hashing (secure storage)
- Security questions for password recovery
- TOTP/QR code two-factor authentication
- Persistent sessions (configurable up to 60 days)
- Device-specific authentication
- All data encrypted and stored locally
- **Zero internet transmission** - complete privacy

### Map Functionality (v0.096.014)
- Interactive map viewer
- Real-time marker placement
- WebSocket-based synchronization
- Click to place markers, click again to remove
- Basic marker types: Enemy, Friendly, Objective, Other
- Clear your own markers
- Multiple simultaneous users

### Map Functionality (v0.099.021 - Upcoming)
- **Zoom in/out with +/- buttons**
- **Ctrl + Mouse Wheel zoom support**
- **Full map scrolling and panning**
- **13 vanilla Arma Reforger marker types**
- **Custom marker shapes** (circles, squares, diamonds, triangles, arrows, stars)
- **Advanced filter system** with individual marker type toggles
- **Improved marker visibility** with proper z-index and rendering

### Server Management
- Configure up to 6 servers
- Store server IP addresses and ports
- Enable/disable servers dynamically
- Server naming and organization
- Switch between servers in real-time
- JSON-based configuration

### Feedback & Community (v0.099.021 - New)
- Built-in feedback submission form
- Bug report and feature request system
- Discord community integration
- Local feedback storage
- Admin dashboard integration (planned for future)

---

## 🚀 Installation

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

## 🔒 Security & Privacy

### Data Protection
- **Local Storage Only**: All data remains on your machine
- **Zero Internet Transmission**: No data sent to external servers
- **Encrypted Passwords**: SHA-256 hashing for password storage
- **Encrypted Security Answers**: Fernet encryption for sensitive data
- **Secure Sessions**: Cryptographically random tokens
- **Device Binding**: Sessions tied to specific devices

### What Data is Stored Locally
- User accounts (username, hashed password)
- Security questions and encrypted answers
- TOTP/QR secrets (encrypted)
- Session tokens
- Server configurations
- Map markers (temporary, for session)
- Feedback submissions (until admin dashboard integration)

### What is NOT Stored or Transmitted
- ❌ Plain text passwords
- ❌ Server credentials or sensitive server information
- ❌ Player positions or game data
- ❌ Personal information beyond what you provide
- ❌ Usage analytics or telemetry

### Database Location
All data stored in: `data/arma_map.db` (SQLite database)

**Note**: Keep this file secure and backed up if needed. Deleting it will remove all user accounts and settings.

---

## 📖 Usage

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

### Using the Map (v0.096.014)

1. Select marker type from dropdown
2. Click on the map to place a marker
3. Click on an existing marker to remove it
4. Markers are synchronized in real-time with other users

### Using the Map (v0.099.021 - New Features)

1. **Zoom Controls**:
   - Click "+" or "−" buttons in toolbar to zoom
   - Or hold **Ctrl** and scroll **Mouse Wheel** up/down
   - Click "Reset" to return to 100% zoom
   
2. **Select Marker Type**:
   - Choose from 13 vanilla Arma Reforger marker types
   - Different shapes for different tactical purposes
   - Enemy, Friendly, Attack, Defend, Pickup, Drop, Meet, Infantry, Armor, Air, Naval, Objective, Other

3. **Place Markers**:
   - Click anywhere on the map to place selected marker type
   - Markers sync instantly to all connected users
   - Different colors and shapes for easy identification

4. **Filter Markers**:
   - Use sidebar on right to show/hide marker types
   - Check/uncheck individual marker types
   - Click "All" to show everything, "None" to hide all

5. **Submit Feedback**:
   - Click "📝 Feedback" button in toolbar
   - Report bugs, request features, or share suggestions
   - Join Discord community for updates

### Submitting Feedback (v0.099.021 - New)

1. Click "📝 Feedback" in the toolbar
2. Fill in subject and feedback details
3. Optionally provide your email
4. Click "Submit Feedback"
5. Join Discord community via the Discord button

**Note**: Feedback is currently stored locally. Admin dashboard integration coming in future update for centralized feedback management.

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
