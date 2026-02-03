# Arma Reforger Live Interactive Map

**THESE APPLICATIONS ONLY WORK ON CERTAIN SERVERS AND CANNOT BE USED ON ANY SERVER USERS WANT, THE SERVERS IN THE CODE ARE FOR SPECIFIC ARMA REFORGER COMMUNITY SERVERS LISTED BELOW:**

**SEVERS THE LIVE MAP WORK ON:**

**MADDOG088 FREEDOM FIGHTERS SERVER**
**VIPER COLLECTIVE MILSIM SERVER**


**Current Version:** 0.096.014 (December 2025)  
**Next Release:** 0.099.021 (2026)

A Windows desktop application for Arma Reforger that provides real-time tactical map viewing, marker placement, and team coordination. Built with Python and PySide6, this portable application keeps all data local and private.

---

## 🎮 Overview

This is a tactical coordination tool for Arma Reforger players, enabling:
- Real-time enemy and objective marker placement
- Live synchronization between multiple users
- Secure local authentication with QR code support
- Multi-server support (up to 6 servers)
- Complete privacy - no data transmitted over internet

---

## 📦 Current Version: 0.096.014

### ✅ Features Implemented

- **Live Map System** - Interactive tactical map with real-time updates
- **4 Marker Types** - Enemy, Friendly, Objective, Other
- **WebSocket Sync** - Instant marker updates across all users
- **Local Authentication** - Secure account system with encrypted storage
- **QR Code Auth** - TOTP/Google Authenticator support
- **Multi-Server** - Configure up to 6 servers
- **Session Management** - "Keep logged in for 60 days" option
- **Dark Theme** - Military-style Arma Reforger aesthetic

---

## 🆕 Next Release: 0.099.021 (2026)

### New Features Coming

- **Map Zoom Controls** - +/- buttons and Ctrl+Mouse Wheel zoom
- **Enhanced Scrolling** - Improved map navigation
- **13 Vanilla Markers** - Full Arma Reforger marker types (Attack, Defend, Pickup, Drop, Meet, Infantry, Armor, Air, Naval, etc.)
- **7 Marker Shapes** - Circle, square, diamond, triangle, arrow, star
- **Advanced Filters** - Show/hide markers by type with sidebar controls
- **Feedback System** - Built-in bug reports and feature requests
- **Discord Integration** - Direct community link (https://discord.gg/ykkkjwDnAD)

---

## 🚀 Quick Start

### Download & Run

1. **Download** the latest release from [GitHub Actions](#) or [Releases](#)
2. **Extract** the ZIP file to any folder
3. **Run** `ArmaReforgerMap.exe`
4. **Create account** and start coordinating!

### For Developers

```bash
cd desktop_app
pip install -r requirements.txt
python main.py
```

---

## 📂 Project Structure

```
arma-reforger-map/
├── desktop_app/           # Main application
│   ├── main.py           # Application entry point
│   ├── core/             # Backend (auth, database, websocket)
│   ├── gui/              # User interface (PySide6)
│   ├── map/              # Map viewer and markers
│   └── config/           # Server configurations
├── .github/
│   └── workflows/
│       └── build.yml     # Automatic .exe builds
└── README.md             # This file
```

---

## 🔒 Security & Privacy

- ✅ **Local Storage Only** - All data remains on your machine
- ✅ **Zero Transmission** - No data sent over internet
- ✅ **Encrypted Storage** - SHA-256 passwords, Fernet encryption
- ✅ **No Tracking** - No analytics or telemetry
- ✅ **Open Source** - Verify security yourself

### What's Stored Locally
- User accounts (encrypted)
- Security questions (encrypted)
- Server configurations
- Session tokens
- Feedback submissions (v0.099.021+)

### What's NOT Stored
- ❌ Plain text passwords
- ❌ Server credentials
- ❌ Personal data beyond what you provide
- ❌ Usage analytics

---

## 🛠️ Building from Source

### Requirements
- Python 3.8+
- PySide6
- See `desktop_app/requirements.txt` for full list

### Build Executable

**Windows:**
```batch
cd desktop_app
build.bat
```

**Linux/Mac:**
```bash
cd desktop_app
chmod +x build.sh
./build.sh
```

**PyInstaller:**
```bash
cd desktop_app
pyinstaller --name "ArmaReforgerMap" --windowed --onedir main.py
```

Output: `desktop_app/dist/ArmaReforgerMap/`

---

## 🤖 Automatic Builds (GitHub Actions)

Every push to `main` triggers an automatic build:

1. ✅ Installs Python 3.11
2. ✅ Installs dependencies
3. ✅ Builds Windows .exe
4. ✅ Creates portable package
5. ✅ Uploads artifacts

**Download:** Go to Actions tab → Latest workflow → Artifacts

**Create Release:**
```bash
git tag v0.099.021
git push origin v0.099.021
```

---

## 📖 Documentation

- **[Complete README](desktop_app/README.md)** - Full documentation
- **[Quick Start Guide](desktop_app/QUICKSTART.md)** - User guide
- **[Changelog](desktop_app/CHANGELOG.md)** - Version history
- **[Setup Guide](desktop_app/SETUP_GUIDE.md)** - GitHub setup
- **[Release Notes](desktop_app/VERSION_0.099.021_RELEASE_NOTES.md)** - Latest features

---

## 🎯 Usage

### First Time
1. Launch application
2. Create account (username + password + security questions)
3. Configure servers in Settings
4. Start placing markers!

### Placing Markers
1. Select marker type from dropdown
2. Click on map to place
3. Click existing marker to remove
4. All users see updates in real-time

### Version 0.099.021 Additions (Coming 2026)
- Zoom with +/− buttons or Ctrl+Wheel
- 13 different marker types with unique shapes
- Filter markers using sidebar
- Submit feedback via built-in form

---

## 💬 Community & Support

- **Discord:** https://discord.gg/ykkkjwDnAD
- **Feedback:** Built into app (v0.099.021+)
- **Issues:** [GitHub Issues](#)

---

## 🗺️ Technology Stack

| Component | Technology |
|-----------|-----------|
| GUI | PySide6 (Qt for Python) |
| Database | SQLite3 |
| Real-Time | WebSockets |
| Auth | PyOTP (TOTP) |
| Encryption | Cryptography (Fernet) |
| Build | PyInstaller |
| CI/CD | GitHub Actions |

---

## 📊 Version Comparison

| Feature | v0.096.014 | v0.099.021 |
|---------|------------|------------|
| Marker Types | 4 | 13 |
| Marker Shapes | 1 | 7 |
| Zoom Controls | ❌ | ✅ |
| Filter System | ❌ | ✅ |
| Feedback Form | ❌ | ✅ |
| Discord Link | ❌ | ✅ |

---

## 🔮 Roadmap

### Version 0.099.021 (2026)
- ✅ Map zoom controls
- ✅ 13 vanilla Arma markers
- ✅ Advanced filter system
- ✅ Feedback system

### Future Versions
- Admin dashboard for feedback
- Cloud sync (optional)
- Real Arma Reforger map images
- Player position tracking
- Voice chat integration
- Squad/team system
- Mobile companion app

---

## 🤝 Contributing

We welcome contributions from the community!

### Ways to Help
- **Test releases** - Report bugs and issues
- **Request features** - Share your ideas
- **Join Discord** - Help other users
- **Spread the word** - Share with your team

### Development
1. Fork the repository
2. Create feature branch
3. Make your changes
4. Submit pull request

---

## 📜 License

MIT License - Free to use, modify, and distribute.

---

## 🙏 Credits

**Developed for the Arma Reforger community**

Special thanks to:
- Beta testers
- Community feedback contributors
- Discord community members
- All Arma Reforger players using this tool

---

## ⚠️ Disclaimer

This application is not affiliated with or endorsed by Bohemia Interactive. Arma Reforger is a trademark of Bohemia Interactive a.s.

Created by and for the community to enhance tactical coordination and teamwork.

---

## 📞 Quick Links

- **[Download Latest Release](#)** - Get the .exe
- **[Full Documentation](desktop_app/README.md)** - Complete guide
- **[Discord Community](https://discord.gg/ykkkjwDnAD)** - Join us
- **[GitHub Actions](../../actions)** - View builds
- **[Changelog](desktop_app/CHANGELOG.md)** - Version history

---

**🎮 Enhance your Arma Reforger tactical coordination today!**
