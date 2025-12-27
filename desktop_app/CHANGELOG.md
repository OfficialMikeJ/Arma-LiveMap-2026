# Changelog

All notable changes to the Arma Reforger Live Interactive Map will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.099.023] - 2026 (In Development)

### Added
- **Real-Time WebSocket Functionality**
  - Enhanced WebSocket server with logging and error handling
  - Player position tracking and synchronization
  - Chat message broadcasting support
  - Ping/pong for connection health monitoring
  - Automatic marker and position sync for new clients
  
- **Arma Server Integration**
  - New `ArmaServerConnector` class for game server communication
  - Simulated player position updates for testing
  - Server info querying (map, player count, status)
  - Foundation for real Arma Reforger API integration

- **Admin Dashboard**
  - Complete feedback management interface
  - View all user submissions in table format
  - Detailed feedback viewer
  - Export feedback to CSV
  - Statistics and filtering

- **Documentation**
  - Comprehensive WebSocket server guide
  - Message protocol documentation
  - Deployment instructions (systemd, Docker)
  - Troubleshooting guide

### Improved
- **WebSocket Client**
  - Better message sending with proper async handling
  - Improved error handling and connection management
  - More robust send_message() implementation

- **Feedback System**
  - Cleaner UI messages
  - Better user communication
  - Updated to version 0.099.023

- **Code Organization**
  - Moved all documentation to `docs/` folder
  - Consolidated scattered .md files
  - Cleaner project root directory

### Fixed
- TOTP disable function now uses proper database connection management
- WebSocket message sending edge cases
- Database connection cleanup in settings window

### Technical
- Added standalone WebSocket server script (`run_websocket_server.py`)
- Created `ArmaServerConnector` for future game integration
- Built admin dashboard for feedback management
- Improved logging throughout WebSocket layer

---

## [0.099.022] - 2026 (In Development)

### Added
- **Custom Server Quick Input**
  - New "Custom Server" button in main toolbar
  - Quick dialog for entering server IP and port
  - Validation for IP addresses and hostnames
  - Option to save servers permanently or connect temporarily
  - Default port (2302) pre-filled for Arma Reforger
  - Support for both IPv4 addresses (192.168.1.100) and hostnames (server.example.com)

### Fixed
- **Database Lock Issue** (CRITICAL FIX)
  - Fixed `sqlite3.OperationalError: database is locked` errors in test suite
  - Implemented proper connection cleanup with try/finally blocks
  - Added 10-second connection timeout to prevent indefinite locks
  - All database methods now guarantee connection closure

### Technical
- Enhanced ServerManager with `add_server()` and `remove_server()` methods
- Improved database connection management across all operations
- Better error handling in database layer

---

## [0.099.021] - 2026 (Planned Release)

### Added
- **Map Zoom Controls**
  - Added +/- zoom buttons in toolbar
  - Implemented Ctrl + Mouse Wheel zoom functionality
  - Added reset zoom button to return to 100%
  - Zoom levels from 25% to 500%
  
- **Enhanced Map Navigation**
  - Improved map scrolling across entire map area
  - Better panning with drag mode
  - Anchor under mouse for natural zoom behavior

- **Vanilla Arma Reforger Markers**
  - Added 13 official marker types:
    - Enemy, Friendly (circles)
    - Attack (arrow), Defend (square)
    - Pickup (triangle up), Drop (triangle down)
    - Meet (star)
    - Infantry (circle), Armor (square)
    - Air (triangle), Naval (diamond)
    - Objective (diamond), Other (circle)
  - Different shapes for each marker type
  - Color-coded markers for quick identification

- **Advanced Filter System**
  - Individual toggle for each marker type
  - Show/hide markers in real-time
  - "Select All" / "Deselect All" quick actions
  - Filter sidebar with all marker types
  - Persistent filter state

- **Feedback System**
  - Built-in feedback submission form
  - Bug report and feature request support
  - Optional email field for follow-up
  - Discord community integration button
  - Local feedback storage (admin dashboard coming later)
  - Direct link to Discord community

### Changed
- Updated marker rendering with improved shapes
- Enhanced UI with sidebar for filters
- Improved toolbar organization
- Better status bar with version info and tips

### Technical
- Version number displayed in title bar
- Better zoom transformation anchoring
- Improved marker visibility management
- Filter state tracking per marker type

---

## [0.096.014] - December 2025

### Initial Release

#### Added
- **Core Application**
  - Desktop application built with PySide6 (Qt for Python)
  - Dark military theme matching Arma Reforger aesthetics
  - Portable - runs without installation

- **Authentication System**
  - Local account creation and management
  - SHA-256 password hashing
  - Encrypted security questions for password recovery
  - Session management with 60-day "keep logged in"
  - TOTP/QR code authentication (Google Authenticator compatible)
  - Device-specific authentication
  - Password reset via security questions

- **Live Map System**
  - Interactive map viewer
  - Real-time marker placement and removal
  - Basic marker types: Enemy, Friendly, Objective, Other
  - Color-coded markers (red, blue, yellow, gray)
  - Click-to-place, click-to-remove interface
  - Grid-based coordinate system

- **Real-Time Communication**
  - WebSocket server for live marker synchronization
  - Minimal latency marker updates
  - Automatic marker sync when joining
  - Supports multiple simultaneous users
  - Connection status indicator

- **Server Management**
  - Configure up to 6 servers
  - Store server IP addresses and ports
  - Enable/disable servers dynamically
  - Server naming and organization
  - JSON-based configuration
  - Easy server switching in UI

- **Security Features**
  - All data stored locally (no internet transmission)
  - Fernet encryption for sensitive data
  - Secure session tokens
  - Encrypted password storage
  - Device-bound sessions

- **Build & Deployment**
  - PyInstaller configuration
  - Windows build scripts (build.bat)
  - Linux/Mac build scripts (build.sh)
  - GitHub Actions workflow for automatic .exe builds
  - Comprehensive documentation

#### Technical Details
- Python 3.11 support
- PySide6 6.6.1 for GUI
- WebSockets 12.0 for real-time sync
- SQLite3 for local database
- Cryptography 41.0.7 for encryption
- PyOTP 2.9.0 for TOTP/QR codes
- QRCode 7.4.2 for QR generation

---

## Version Numbering

The version numbering follows the format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Significant changes or complete rewrites
- **MINOR**: New features and enhancements
- **PATCH**: Bug fixes and minor improvements

Example: `0.099.021`
- `0` = Major version (pre-1.0 development)
- `099` = Minor version (feature updates)
- `021` = Patch version (bug fixes)

---

## Upcoming Features (Future Versions)

### Planned for Post-0.099.021
- Admin dashboard for feedback management
- Cloud sync for markers (optional)
- Voice chat integration
- Squad/team grouping
- Marker notes and timestamps
- Export marker history
- Multiple map support per server
- Import real Arma Reforger map images
- Player position tracking from game servers
- Mobile companion app
- Customizable marker colors and sizes

### Under Consideration
- Plugin system for extensions
- Custom marker types
- Drawing tools on map
- Measurement tools (distance, bearing)
- Waypoint system
- Integration with Arma Reforger RCON
- Replay/history mode
- Statistics and analytics
- Multi-language support

---

## Support & Community

- **Discord**: https://discord.gg/ykkkjwDnAD
- **GitHub Issues**: [Report bugs or request features]
- **Documentation**: See README.md and QUICKSTART.md

---

## Credits

Developed for the Arma Reforger community to enhance tactical coordination and teamwork.

Thank you to all beta testers and community members for their feedback and support!
