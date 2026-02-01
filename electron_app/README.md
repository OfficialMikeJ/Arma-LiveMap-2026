# Arma Reforger Tactical Map - Electron Desktop App

**Version:** 1.0.0  
**Platform:** Windows, Linux, macOS  
**Technology:** Electron + React + TypeScript + Tailwind CSS

---

## Features

✅ **Authentication System**
- Local account creation
- SHA-256 password hashing
- Security questions for password recovery
- TOTP/QR code 2FA support
- 60-day session management

✅ **Tactical Map**
- Interactive canvas-based map
- 13 marker types (Enemy, Friendly, Attack, Defend, Pickup, Drop, Meet, Infantry, Armor, Air, Naval, Objective, Other)
- 7 marker shapes (Circle, Square, Diamond, Triangle, Arrow, Star, Polygon)
- Click to place markers
- Click existing markers to remove

✅ **Real-time Synchronization**
- WebSocket server for instant marker sync between users
- Connection status indicator
- Live player count

✅ **Map Controls**
- Zoom in/out (+/- buttons)
- Zoom reset
- Pan with right-click drag
- Ctrl + Mouse Wheel zoom (coming soon)

✅ **Filter System**
- Show/hide markers by type
- Select all / Deselect all
- Filter sidebar

✅ **Feedback System**
- Submit bug reports
- Feature requests
- Suggestions
- Discord community link

✅ **Dark Military Theme**
- Professional Arma Reforger aesthetic
- High contrast for readability

---

## Installation & Setup

### Prerequisites
- Node.js 18+ and npm/yarn
- Windows 10/11, Linux, or macOS

### Install Dependencies
```bash
cd electron_app
yarn install
```

### Development Mode
```bash
yarn start
```
This starts both the React dev server and Electron app.

### Build for Production

**Windows:**
```bash
yarn build:win
```

**Linux:**
```bash
yarn build:linux
```

**macOS:**
```bash
yarn build:mac
```

Output will be in `electron_app/release/` directory.

---

## Project Structure

```
electron_app/
├── electron/              # Electron main process
│   ├── main.ts           # App entry point
│   ├── database.ts       # SQLite database service
│   ├── auth.ts           # Authentication service
│   ├── websocket-server.ts  # WebSocket server
│   └── preload.ts        # Preload script (IPC bridge)
├── src/                   # React renderer process
│   ├── components/       # React components
│   │   ├── MapCanvas.tsx
│   │   ├── ToolBar.tsx
│   │   ├── MarkerTypeSelector.tsx
│   │   └── FilterSidebar.tsx
│   ├── pages/            # Page components
│   │   ├── LoginPage.tsx
│   │   └── MapPage.tsx
│   ├── types/            # TypeScript types
│   ├── styles/           # CSS styles
│   ├── App.tsx           # Main App component
│   └── main.tsx          # React entry point
├── dist/                  # Build output
├── release/               # Packaged executables
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md             # This file
```

---

## Database Schema

The app uses SQLite for local data storage:

**Users Table:**
- id, username, password_hash, totp_secret, created_at

**Security Questions Table:**
- id, user_id, question, answer_hash

**Sessions Table:**
- id, user_id, token, device_id, expires_at

**Servers Table:**
- id, name, ip_address, port, enabled

**Markers Table:**
- id, type, shape, x, y, color, created_by, timestamp, notes

**Feedback Table:**
- id, type, message, email, submitted_at

Database file location: `%APPDATA%/arma-reforger-tactical-map/tacmap.db` (Windows)

---

## WebSocket Protocol

**Port:** 8765  
**Protocol:** ws://

**Message Format:**
```json
{
  "type": "marker",
  "action": "add" | "remove",
  "data": {
    "id": "marker-id",
    "type": "enemy",
    "x": 5000,
    "y": 3000,
    ...
  },
  "timestamp": "2025-01-10T14:30:00Z"
}
```

---

## Keyboard Shortcuts

- **Ctrl + Mouse Wheel:** Zoom in/out (coming soon)
- **Right Click + Drag:** Pan map
- **Click:** Place marker
- **Click on Marker:** Remove marker

---

## Server Configuration

Default test server is pre-configured:
- **IP:** 192.168.2.26
- **Port:** 2001

Additional servers can be added in Settings (up to 6 total).

---

## Troubleshooting

**App won't start:**
- Ensure all dependencies are installed: `yarn install`
- Check Node.js version: `node --version` (should be 18+)

**WebSocket not connecting:**
- Check if port 8765 is available
- Firewall may be blocking the port

**Build fails:**
- Delete `node_modules` and `dist` folders
- Run `yarn install` again
- Try building again

**Markers not syncing:**
- Check WebSocket status indicator (green = connected)
- Click Refresh button
- Restart the app

---

## Future Enhancements

- Server management UI
- Advanced TOTP settings
- Export/import marker data
- Custom map images
- Voice chat integration
- Mobile companion app integration

---

## License

MIT License - Free to use, modify, and distribute.

---

## Support

- **Discord:** https://discord.gg/ykkkjwDnAD
- **Feedback:** Use built-in feedback form
- **GitHub:** [Repository URL]

---

**🎮 Enhance your Arma Reforger tactical coordination!**
