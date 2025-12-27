# Arma Reforger Live Interactive Map

**Current Version:** 0.099.022 (In Development)  
**Latest Stable:** 0.096.014 (December 2025)

---

## Overview

A Windows desktop application for Arma Reforger that provides real-time tactical map viewing and coordination capabilities. Built with Python and PySide6, this portable application runs locally without requiring installation, keeping all your data private and secure.

---

## Current Version: 0.096.014

### Features Implemented

#### Authentication & Security
- ✅ **Local Account System**
  - Create accounts with username and password
  - SHA-256 password hashing for secure storage
  - Encrypted security questions for password recovery
  - No data transmitted over internet - complete privacy

- ✅ **Two-Factor Authentication**
  - TOTP/QR code authentication using Google Authenticator
  - Optional enhanced security layer
  - Encrypted TOTP secrets

- ✅ **Session Management**
  - "Keep me logged in for 60 days" option
  - Device-specific session tokens
  - Secure cryptographically random tokens

#### Live Map System
- ✅ **Interactive Map Viewer**
  - Real-time tactical map display
  - Grid-based coordinate system
  - Click to place markers
  - Click existing markers to remove

- ✅ **Real-Time Marker Synchronization**
  - WebSocket-based instant updates
  - Minimal latency between users
  - Automatic sync when joining
  - Support for multiple simultaneous users

- ✅ **Basic Marker Types** (4 types)
  - Enemy (Red circles)
  - Friendly (Blue circles)
  - Objective (Yellow circles)
  - Other (Gray circles)

- ✅ **Connection Status**
  - Real-time connection indicator
  - Player count display
  - Connection health monitoring

#### Server Management
- ✅ **Multi-Server Support**
  - Configure up to 6 servers
  - Store IP addresses and ports
  - Enable/disable servers dynamically
  - Quick server switching

- ✅ **Server Configuration**
  - Custom server names
  - JSON-based persistent storage
  - Easy management through Settings UI

#### User Interface
- ✅ **Dark Military Theme**
  - Professional Arma Reforger aesthetic
  - Military green accent colors
  - High contrast for readability

- ✅ **Simple Controls**
  - Toolbar with quick access buttons
  - Clear marker management
  - Intuitive server selection

---

## Upcoming Version: 0.099.021 (2026)

### New Features Planned

#### Enhanced Map Controls
- 🆕 **Map Zoom System**
  - Zoom in/out with +/- buttons in toolbar
  - Ctrl + Mouse Wheel zoom support
  - Reset zoom button (return to 100%)
  - Zoom range: 25% to 500%
  - Smooth zoom transitions

- 🆕 **Enhanced Map Navigation**
  - Improved scrolling across entire map area
  - Better panning with drag mode
  - Zoom anchors under mouse cursor for natural feel
  - Optimized viewport management

#### Expanded Marker System
- 🆕 **Vanilla Arma Reforger Markers** (13 types total)
  - **Tactical Markers:**
    - Enemy (Red circle)
    - Friendly (Blue circle)
    - Attack (Red arrow - indicates direction)
    - Defend (Blue square - hold position)
  
  - **Coordination Markers:**
    - Pickup (Green triangle ▲ - extraction points)
    - Drop (Red triangle ▼ - drop zones)
    - Meet (Purple star ★ - rendezvous points)
  
  - **Unit Type Markers:**
    - Infantry (Green circle)
    - Armor (Yellow square - vehicles)
    - Air (Light blue triangle - aircraft)
    - Naval (Blue diamond - boats/ships)
  
  - **Mission Markers:**
    - Objective (Yellow diamond - mission goals)
    - Other (Gray circle - general purpose)

- 🆕 **Visual Marker Improvements**
  - 7 different marker shapes for instant recognition
  - Color-coded system matching Arma Reforger
  - White outlines for better visibility
  - Consistent sizing and rendering

#### Advanced Filter System
- 🆕 **Marker Filtering**
  - Filter sidebar with all marker types
  - Individual toggle for each marker type
  - Real-time show/hide functionality
  - No performance impact on filtering

- 🆕 **Quick Filter Actions**
  - "Select All" button - show all marker types
  - "Deselect All" button - hide all markers
  - Filter state persists across sessions

- 🆕 **Tactical View Customization**
  - Hide friendly markers to focus on threats
  - Show only objectives during planning
  - Create custom views for different roles
  - Reduce map clutter in busy operations

#### Feedback & Community
- 🆕 **Built-in Feedback System**
  - Submit bug reports directly from app
  - Request features and improvements
  - Share suggestions with development team
  - Optional email for follow-up

- 🆕 **Discord Integration**
  - Direct link to community Discord server
  - One-click access to updates and announcements
  - Community support and coordination
  - Link: https://discord.gg/ykkkjwDnAD

- 🆕 **Local Feedback Storage**
  - Feedback saved locally for privacy
  - Admin dashboard integration coming later
  - All submissions timestamped and organized

#### User Experience Improvements
- 🆕 **Enhanced Toolbar**
  - Better organization of controls
  - Zoom controls prominently displayed
  - Quick access to feedback system
  - Version number in title bar

- 🆕 **Helpful Tips**
  - Status bar tooltips
  - "Ctrl + Mouse Wheel to zoom" reminder
  - Version information displayed
  - Better user guidance

---

## Installation

### Requirements
- **Operating System:** Windows 10/11, Linux, or macOS
- **Python:** 3.8 or higher (for development)
- **RAM:** 256MB minimum
- **Storage:** 50MB for application + data

### Dependencies
```
PySide6==6.6.1
websockets==12.0
pyotp==2.9.0
qrcode[pil]==7.4.2
cryptography==41.0.7
Pillow==10.1.0
requests==2.31.0
aiohttp==3.9.1
```

### Setup (Development)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

### Building Executable

**Windows:**
```batch
build.bat
```

**Linux/Mac:**
```bash
chmod +x build.sh
./build.sh
```

**Manual PyInstaller:**
```bash
pyinstaller --name "ArmaReforgerMap" --windowed --onedir main.py
```

The executable will be in: `dist/ArmaReforgerMap/`

---

## Usage

### First Time Setup

1. **Launch the application**
2. **Create an account:**
   - Click "Create Account"
   - Enter username and password (minimum 4 characters)
   - Answer 2 security questions
   - Click OK
3. **Login** with your new credentials

### Setting Up QR Code Authentication (Optional)

1. Login and click **"Settings"** in the toolbar
2. Click **"Enable QR Authentication"**
3. Scan the QR code with Google Authenticator or similar app
4. Enter the 6-digit verification code
5. On future logins, check **"Keep me logged in for 60 days"**

### Configuring Servers

1. Click **"Settings"** in the toolbar
2. **Enable** the server slots you want to use (up to 6)
3. For each server:
   - Enter server name (e.g., "Main Server")
   - Enter IP address (e.g., "192.168.1.100")
   - Enter port number (e.g., "2302")
4. Click **"Save Server Configuration"**

### Using the Map (Current Version 0.096.014)

1. **Select marker type** from dropdown (Enemy, Friendly, Objective, Other)
2. **Click on the map** to place a marker
3. **Click on an existing marker** to remove it
4. Markers are **synchronized in real-time** with all connected users

### Using the Map (Version 0.099.021 - Coming 2026)

1. **Zoom the map:**
   - Click **+** or **−** buttons in toolbar
   - Or hold **Ctrl** and scroll **Mouse Wheel**
   - Click **⟲ Reset** to return to 100%

2. **Select marker type:**
   - Choose from 13 vanilla Arma Reforger marker types
   - Different shapes for different tactical purposes
   - Attack, Defend, Pickup, Drop, Meet, Infantry, Armor, Air, Naval, etc.

3. **Place markers:**
   - Click anywhere on the map to place selected marker
   - Markers sync instantly to all users
   - Different colors and shapes for easy identification

4. **Filter markers:**
   - Use the **sidebar on right** to show/hide marker types
   - Check/uncheck individual marker types
   - Click **"All"** to show everything, **"None"** to hide all

5. **Submit feedback:**
   - Click **"📝 Feedback"** button in toolbar
   - Report bugs, request features, or share suggestions
   - Join Discord community for updates

---

## Data Storage

All data is stored locally in the `data/` folder:

```
data/
├── arma_map.db          # SQLite database (users, sessions, markers)
├── .key                 # Encryption key for sensitive data
├── .device_id           # Unique device identifier
├── .session             # Current session token
└── feedback/            # Feedback submissions (v0.099.021+)
    └── feedback_submissions.json
```

### What is Stored
- User accounts (username, hashed password)
- Security questions (encrypted answers)
- TOTP secrets (encrypted)
- Session tokens and expiration dates
- Server configurations
- Temporary marker data during sessions
- Feedback submissions (local, for future admin dashboard)

### What is NOT Stored or Transmitted
- ❌ Plain text passwords
- ❌ Server login credentials
- ❌ Game data or player positions
- ❌ Usage analytics or telemetry
- ❌ Personal information beyond what you provide

---

## Security & Privacy

### Data Protection
- **SHA-256 Password Hashing** - Passwords never stored in plain text
- **Fernet Encryption** - Security answers and TOTP secrets encrypted
- **Local Storage Only** - Zero data transmission over internet
- **Secure Sessions** - Cryptographically random tokens
- **Device Binding** - Sessions tied to specific devices

### Privacy Guarantee
✅ All data remains on your machine  
✅ No external servers or cloud services  
✅ No analytics or tracking  
✅ Complete privacy and control  
✅ Open source code - verify for yourself  

### Security Best Practices
- Keep your `data/` folder backed up
- Use strong passwords (8+ characters recommended)
- Enable QR/TOTP authentication for enhanced security
- Don't share your device's `data/` folder
- Delete `.session` file if switching devices

---

## Building with GitHub Actions

The project includes automated builds via GitHub Actions.

### Automatic Build on Push

1. Push your code to GitHub
2. GitHub Actions automatically:
   - Installs Python 3.11
   - Installs all dependencies
   - Builds .exe with PyInstaller
   - Creates portable package
   - Uploads artifacts

3. Download from **Actions** tab → Latest workflow → **Artifacts**

### Creating a Release

```bash
git tag v0.099.021
git push origin v0.099.021
```

This creates a GitHub Release with attached .exe file.

---

## Technical Architecture

### Technology Stack
- **GUI Framework:** PySide6 (Qt for Python)
- **Database:** SQLite3 (built-in)
- **Real-Time:** WebSockets 12.0
- **Authentication:** PyOTP 2.9.0 (TOTP/QR codes)
- **Encryption:** Cryptography 41.0.7 (Fernet)
- **QR Codes:** qrcode 7.4.2 + Pillow 10.1.0
- **Packaging:** PyInstaller (for .exe)

### Application Structure
```
desktop_app/
├── main.py                    # Application entry point
├── core/                      # Backend logic
│   ├── auth.py               # TOTP authentication
│   ├── database.py           # SQLite operations
│   ├── encryption.py         # Security functions
│   ├── websocket_server.py   # Real-time sync
│   └── server_manager.py     # Server configuration
├── gui/                       # User interface
│   ├── login_window.py       # Login screen
│   ├── main_window.py        # Main application
│   ├── settings_window.py    # Settings dialog
│   ├── feedback_dialog.py    # Feedback form (v0.099.021+)
│   └── styles.py             # Dark theme
├── map/                       # Map system
│   └── map_viewer.py         # Interactive map
└── config/
    └── servers.json          # Server configurations
```

---

## Troubleshooting

### Common Issues

**"Cannot connect to WebSocket server"**
- WebSocket server starts automatically on app launch
- Check firewall settings if connection fails
- Verify port 8765 is not in use by another application

**"Invalid username or password"**
- Usernames and passwords are case-sensitive
- Use "Forgot Password?" to reset via security questions
- Create a new account if needed

**"QR code not working"**
- Ensure device time is synchronized
- Try entering the manual key instead of scanning
- Use "Disable QR Authentication" in Settings and set up again

**"Markers not syncing"**
- Check connection status indicator (should show green checkmark)
- Click "Refresh" button in toolbar
- Restart the application if issue persists

---

## Contributing

This is a community-driven project for Arma Reforger players.

### How to Contribute
1. **Report Bugs** - Use the built-in feedback system (v0.099.021+)
2. **Request Features** - Share your ideas via feedback form
3. **Join Discord** - https://discord.gg/ykkkjwDnAD
4. **Test Releases** - Help test new features before release

### Planned Future Features
- Admin dashboard for feedback management
- Cloud sync option (optional)
- Import real Arma Reforger map images
- Player position tracking from game servers
- Voice chat integration
- Squad/team grouping system
- Marker notes and timestamps
- Export marker history
- Mobile companion app

---

## Version History

### Version 0.096.014 (December 2025) - Current
- Initial public release
- Core authentication system
- Basic marker types (4 types)
- Real-time WebSocket synchronization
- Server management (up to 6 servers)
- TOTP/QR code authentication
- Dark military theme

### Version 0.099.021 (2026) - Upcoming
- Map zoom controls (+/- buttons, Ctrl+Wheel)
- Enhanced map scrolling
- Vanilla Arma Reforger markers (13 types)
- Advanced filter system
- Built-in feedback system
- Discord community integration

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

---

## Support & Community

### Get Help
- **Discord:** https://discord.gg/ykkkjwDnAD
- **Feedback System:** Built into app (v0.099.021+)
- **Documentation:** This README and QUICKSTART.md

### Stay Updated
- Join our Discord for development updates
- Follow releases on GitHub
- Participate in beta testing

---

## License

MIT License - Free to use, modify, and distribute.

---

## Credits

Developed for the Arma Reforger community to enhance tactical coordination and teamwork.

**Special Thanks:**
- Beta testers and early adopters
- Community feedback contributors
- Discord community members

---

## Disclaimer

This application is not affiliated with or endorsed by Bohemia Interactive. Arma Reforger is a trademark of Bohemia Interactive a.s.

This tool is created by and for the community to enhance gameplay coordination. All data remains local to your machine.
