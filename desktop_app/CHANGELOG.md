# Changelog

All notable changes to the Arma Reforger Live Interactive Map will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
