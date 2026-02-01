# Arma Reforger Tactical Map System - Full Production Architecture

**Version:** 1.0.0  
**Last Updated:** January 2025  
**Target Platform:** Windows Desktop (Electron), Android Mobile, Arma Reforger Game Server

---

## 📋 Project Overview

This is a **real-time tactical coordination system** for Arma Reforger that provides synchronized map viewing, marker placement, and team coordination across multiple platforms:

- **Desktop Application** (Electron + React + TypeScript)
- **Mobile Application** (Native Android + Kotlin)
- **Game Server Mod** (Arma Reforger Workshop Mod - To Be Developed)

### Core Goal
Enable players to view and place tactical markers in real-time that synchronize between:
1. Desktop users running the Electron app
2. Mobile users running the Android app  
3. In-game players connected to the Arma Reforger server with the mod installed

---

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARMA REFORGER GAME SERVER                    │
│                    IP: 192.168.2.26                             │
│                    Ports: 2001, 17777, 19999                    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         CUSTOM WORKSHOP MOD (To Be Developed)            │  │
│  │  - Listens for external connections                      │  │
│  │  - Receives marker data from apps                        │  │
│  │  - Broadcasts markers to in-game players                 │  │
│  │  - Sends game events back to apps                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ▲                                    │
│                            │                                    │
│                    Communication Protocol                       │
│                    (REST API / WebSocket)                       │
│                            │                                    │
└────────────────────────────┼───────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
    ┌─────────────────┐           ┌─────────────────┐
    │  ELECTRON APP   │           │   ANDROID APP   │
    │  (Desktop PC)   │◄─────────►│    (Mobile)     │
    │                 │           │                 │
    │  WebSocket Sync │           │  WebSocket Sync │
    │  between users  │           │  between users  │
    └─────────────────┘           └─────────────────┘
            ▲                             ▲
            │                             │
            └─────────────┬───────────────┘
                          │
                  Internal User Sync
                  (App-to-App without
                   game server)
```

### Communication Layers

#### Layer 1: App-to-App Synchronization (EXISTING)
- **Purpose**: Sync markers between desktop and mobile users without game server
- **Protocol**: WebSocket (ws:// or wss://)
- **Port**: 8765 (configurable)
- **Use Case**: Standalone tactical planning without being in-game

#### Layer 2: App-to-GameServer Communication (TO BE IMPLEMENTED)
- **Purpose**: Send/receive markers to/from Arma Reforger server mod
- **Protocol**: REST API and/or WebSocket (to be determined by mod capabilities)
- **Ports**: 2001, 17777, 19999 (or custom port for mod API)
- **Use Case**: Real-time integration with live game session

---

## 🎯 Full Production Workflow

### Scenario: Team Tactical Operation

**Setup Phase:**
1. Server admin installs the custom Arma Reforger Workshop mod
2. Server starts with mod enabled on 192.168.2.26
3. Mod exposes an API endpoint (e.g., `http://192.168.2.26:2001/api/markers`)

**User Experience:**

**Desktop User (Squad Leader at Base):**
1. Opens Electron app on Windows PC
2. Logs in with credentials + 2FA
3. Configures server: `192.168.2.26:2001`
4. Connects to game server
5. Places "Enemy" marker at grid coordinates
6. Marker instantly appears:
   - On all connected mobile devices
   - On all other desktop users
   - **In-game for players with the mod installed**

**Mobile User (Field Operator):**
1. Opens Android app on phone/tablet
2. Logs in with same credentials (synced accounts)
3. App auto-connects to configured server
4. Sees the enemy marker placed by squad leader
5. Places "Pickup" marker for extraction point
6. Marker syncs back to desktop and in-game players

**In-Game Player:**
1. Joins Arma Reforger server with mod installed
2. Opens tactical map in-game (via mod UI)
3. Sees all markers placed by desktop/mobile users
4. Can place markers in-game that sync to apps
5. Receives real-time updates as team moves

---

## 🔧 Technical Specifications

### Desktop Application (Electron)

**Technology Stack:**
- **Framework**: Electron 28+
- **UI**: React 18 + TypeScript
- **Styling**: Tailwind CSS (Dark Military Theme)
- **Database**: SQLite3 (better-sqlite3)
- **WebSocket**: ws library
- **HTTP Client**: axios
- **Build**: electron-builder

**Features:**
- ✅ Local authentication (SHA-256 hashing)
- ✅ TOTP/QR code 2FA (Google Authenticator)
- ✅ Session management (60-day keep-alive)
- ✅ 13 marker types with 7 shapes
- ✅ Zoom controls (+/-, Ctrl+Wheel)
- ✅ Pan/scroll navigation
- ✅ Real-time marker sync (WebSocket)
- ✅ Server configuration (up to 6 servers)
- ✅ Marker filtering system
- ✅ Feedback submission
- ✅ Discord integration

**Database Schema:**
```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    totp_secret TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Security questions
CREATE TABLE security_questions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    question TEXT,
    answer_hash TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Sessions
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    token TEXT UNIQUE,
    device_id TEXT,
    expires_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Servers
CREATE TABLE servers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    ip_address TEXT,
    port INTEGER,
    enabled BOOLEAN DEFAULT 1
);

-- Markers (temporary cache)
CREATE TABLE markers (
    id TEXT PRIMARY KEY,
    type TEXT,
    x REAL,
    y REAL,
    created_by TEXT,
    timestamp DATETIME
);
```

---

### Android Application (Native Kotlin)

**Technology Stack:**
- **Language**: Kotlin
- **UI**: Jetpack Compose (Material Design 3)
- **Database**: Room (SQLite wrapper)
- **WebSocket**: OkHttp + Scarlet
- **HTTP**: Retrofit2
- **Architecture**: MVVM + Repository Pattern
- **Security**: AndroidX Security (EncryptedSharedPreferences)
- **QR Codes**: ZXing (com.google.zxing)
- **Build**: Gradle 8+

**Features:**
- ✅ Same authentication as desktop
- ✅ TOTP/QR code scanning
- ✅ Biometric login (fingerprint/face)
- ✅ Pinch-to-zoom on map
- ✅ Touch gestures for pan
- ✅ Real-time marker sync
- ✅ Push notifications for marker updates (optional)
- ✅ Offline mode with sync on reconnect
- ✅ Material Design 3 dark theme

**Minimum Android Version:** Android 8.0 (API 26)  
**Target Android Version:** Android 14 (API 34)

---

### Arma Reforger Game Server Mod (TO BE DEVELOPED)

**Technology Stack:**
- **Engine**: Enfusion Engine
- **Language**: Enforce Script (C#-like)
- **Framework**: EnfusionDatabaseFramework (optional)
- **Distribution**: Arma Reforger Workshop

**Required Capabilities:**

#### 1. API Endpoints (REST)
The mod should expose HTTP endpoints:

```
POST /api/markers
- Receive marker data from apps
- Body: JSON with marker details
- Returns: Success/failure status

GET /api/markers
- Send current markers to apps
- Returns: JSON array of all markers

DELETE /api/markers/{id}
- Remove marker by ID
- Returns: Success status

GET /api/status
- Server health check
- Returns: Player count, server status

WS /api/sync (Optional WebSocket)
- Real-time bidirectional marker sync
- Broadcasts marker events to all connected apps
```

#### 2. In-Game Features
- **Map UI**: Custom tactical map overlay (or integration with game map)
- **Marker Placement**: Players can place markers in-game via UI
- **Marker Rendering**: Show markers from apps on in-game map
- **Permissions**: Admin-only marker deletion
- **Notifications**: Alert players when new markers appear

#### 3. Data Format

**Marker JSON Structure:**
```json
{
  "id": "uuid-v4-string",
  "type": "enemy|friendly|attack|defend|pickup|drop|meet|infantry|armor|air|naval|objective|other",
  "shape": "circle|square|diamond|triangle|arrow|star|polygon",
  "position": {
    "x": 5250.5,
    "y": 3120.8,
    "grid": "E5-2-3"
  },
  "color": "#FF0000",
  "created_by": "username",
  "timestamp": "2025-01-10T14:30:00Z",
  "notes": "Enemy patrol spotted"
}
```

**Server Info JSON:**
```json
{
  "server_name": "My Reforger Server",
  "player_count": 12,
  "max_players": 64,
  "map": "Everon",
  "game_mode": "Conflict",
  "api_version": "1.0.0",
  "mod_version": "0.1.0"
}
```

#### 4. Integration Points

**Apps → Mod Communication:**
```
1. App authenticates user locally
2. App connects to http://192.168.2.26:2001/api/
3. App sends POST request when user places marker
4. Mod receives marker data
5. Mod broadcasts to in-game players via Enfusion replication
```

**Mod → Apps Communication:**
```
1. Player places marker in-game via mod UI
2. Mod sends marker data to all connected apps via WebSocket
   OR apps poll GET /api/markers every 2 seconds
3. Apps update local marker cache
4. Apps render marker on tactical map
```

#### 5. Configuration File
The mod should include a config file for admins:

```json
{
  "api_enabled": true,
  "api_port": 2001,
  "websocket_enabled": true,
  "websocket_port": 19999,
  "require_auth": false,
  "admin_password": "changeme",
  "max_markers": 500,
  "marker_expiry_seconds": 3600,
  "allowed_marker_types": ["all"],
  "logging_enabled": true
}
```

---

## 🔐 Security Considerations

### App-Level Security
- ✅ SHA-256 password hashing (minimum)
- ✅ Argon2 recommended for production
- ✅ TOTP 2FA with encrypted secrets
- ✅ Session tokens (cryptographically random)
- ✅ Device binding for sessions
- ✅ No plain-text password storage

### Network Security
- ⚠️ Currently using HTTP (local network)
- 🔒 HTTPS/TLS recommended for production
- 🔒 API key authentication for mod endpoints
- 🔒 Rate limiting to prevent spam
- 🔒 Input validation on all endpoints

### Game Server Mod Security
- Admin-only marker deletion
- Rate limiting on marker placement
- Maximum marker count enforcement
- Payload size limits
- Optional authentication token requirement

---

## 📊 Data Flow Diagrams

### Marker Placement Flow

```
User Action: Places "Enemy" marker at position (5250, 3120)
                           │
                           ▼
              ┌────────────────────────┐
              │  Desktop/Mobile App    │
              │  1. Validate position  │
              │  2. Generate UUID      │
              │  3. Create marker JSON │
              └────────────────────────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
    ┌───────────────┐           ┌────────────────┐
    │   Local DB    │           │  WebSocket     │
    │   Store copy  │           │  Broadcast to  │
    │               │           │  other apps    │
    └───────────────┘           └────────────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │ Game Server Mod API │
                              │ POST /api/markers   │
                              │ Store in mod cache  │
                              └─────────────────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │  In-Game Players    │
                              │  Receive marker via │
                              │  Enfusion network   │
                              └─────────────────────┘
```

---

## 🚀 Deployment Architecture

### Development Environment
```
Local Machine (192.168.2.26)
├── Arma Reforger Server (ports 2001, 17777, 19999)
├── Custom Workshop Mod (to be installed)
├── Electron App (running on desktop)
└── Android App (running on phone/tablet via USB debugging)
```

### Production Environment
```
Dedicated Server (Public IP)
├── Arma Reforger Server
│   ├── Game Port: 2001 (UDP)
│   ├── Query Port: 17777 (UDP)
│   └── Steam Port: 19999 (UDP/TCP)
├── Mod API Endpoints
│   ├── HTTP: Port 8080 (TCP)
│   └── WebSocket: Port 8765 (TCP)
├── Firewall Rules
│   ├── Allow: 2001, 17777, 19999, 8080, 8765
│   └── Block: All other ports
└── SSL/TLS Certificate (for HTTPS)
```

### Scalability
- **App-to-App Sync**: P2P or relay server for 100+ users
- **Game Server**: Single instance supports 64 players
- **API Load**: Can handle 1000+ requests/minute with caching
- **Database**: SQLite sufficient for 10,000+ markers

---

## 🧪 Testing Strategy

### Test Server Configuration
- **IP**: 192.168.2.26 (local network)
- **Ports**: 2001, 17777, 19999
- **Latency**: <50ms (local)
- **Test Users**: 5-10 concurrent

### Test Scenarios

**Scenario 1: Standalone App Sync**
1. Open desktop app on PC1
2. Open desktop app on PC2
3. Place marker on PC1
4. Verify marker appears on PC2 within 1 second
5. Delete marker on PC2
6. Verify deletion syncs to PC1

**Scenario 2: Cross-Platform Sync**
1. Open desktop app
2. Open Android app
3. Place marker on desktop
4. Verify marker appears on Android
5. Place marker on Android
6. Verify marker appears on desktop

**Scenario 3: Game Server Integration** (Once mod is ready)
1. Start Arma Reforger server with mod
2. Open desktop app, connect to server
3. Place marker in app
4. Verify marker appears in-game
5. Place marker in-game via mod UI
6. Verify marker appears in app

**Scenario 4: Stress Test**
1. Place 500 markers rapidly
2. Monitor app performance (should remain <100ms lag)
3. Monitor server CPU/memory usage
4. Verify no markers lost

---

## 📝 Implementation Phases

### Phase 1: App Development (CURRENT)
- ✅ Build Electron desktop app
- ✅ Build Android mobile app
- ✅ Implement app-to-app WebSocket sync
- ✅ Test standalone functionality
- ✅ Deploy for initial user testing

### Phase 2: Mod Development (NEXT)
- ⬜ Learn Enfusion scripting
- ⬜ Create basic Workshop mod
- ⬜ Implement HTTP REST API endpoints
- ⬜ Test marker placement from apps
- ⬜ Add in-game marker rendering

### Phase 3: Integration Testing
- ⬜ Connect apps to game server mod
- ⬜ Test bidirectional marker sync
- ⬜ Stress test with multiple users
- ⬜ Fix bugs and optimize performance

### Phase 4: Production Deployment
- ⬜ Publish mod to Workshop
- ⬜ Release desktop app (GitHub / website)
- ⬜ Release Android app (Google Play / APK)
- ⬜ Create user documentation
- ⬜ Setup community Discord server

---

## 🛠️ Developer Notes

### For Mod Developer (Enfusion Script)

**Key Challenges:**
1. Enfusion has no built-in HTTP server - may need external middleware
2. Option A: Run a separate Node.js/Python server alongside Arma server
3. Option B: Use EnfusionDatabaseFramework with custom REST adapter
4. Option C: File-based communication (apps write JSON, mod reads)

**Recommended Approach:**
```
┌─────────────────┐
│  Arma Reforger  │
│  + Custom Mod   │
└────────┬────────┘
         │ (File I/O or Network RPC)
         ▼
┌─────────────────┐
│  Middleware     │
│  Node.js/Python │
│  HTTP Server    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Desktop/Mobile │
│  Apps           │
└─────────────────┘
```

**Middleware Server (Express.js example):**
```javascript
const express = require('express');
const fs = require('fs');
const app = express();

app.use(express.json());

// Shared JSON file with Arma mod
const MARKER_FILE = 'C:/ArmaReforger/markers.json';

app.post('/api/markers', (req, res) => {
  const markers = JSON.parse(fs.readFileSync(MARKER_FILE));
  markers.push(req.body);
  fs.writeFileSync(MARKER_FILE, JSON.stringify(markers));
  res.json({ success: true });
});

app.get('/api/markers', (req, res) => {
  const markers = JSON.parse(fs.readFileSync(MARKER_FILE));
  res.json(markers);
});

app.listen(2001, () => console.log('Middleware on port 2001'));
```

**Enfusion Mod (Pseudo-code):**
```cpp
class TacticalMapMod : ScriptComponent
{
    protected const string MARKER_FILE = "$profile:markers.json";
    protected ref array<ref TacMarker> m_Markers;
    
    void Init()
    {
        GetGame().GetCallqueue().CallLater(SyncMarkers, 2000, true);
    }
    
    void SyncMarkers()
    {
        // Read markers from JSON file
        FileHandle file = FileIO.OpenFile(MARKER_FILE, FileMode.READ);
        string json = file.ReadString();
        file.Close();
        
        // Parse and update in-game markers
        m_Markers = JsonSerializer.ParseArray(json);
        
        // Broadcast to all clients
        foreach (TacMarker marker : m_Markers)
        {
            RenderMarkerOnMap(marker);
        }
    }
    
    void OnPlayerPlaceMarker(TacMarker marker)
    {
        // Write to JSON file for apps to read
        m_Markers.Insert(marker);
        string json = JsonSerializer.Stringify(m_Markers);
        
        FileHandle file = FileIO.OpenFile(MARKER_FILE, FileMode.WRITE);
        file.WriteString(json);
        file.Close();
    }
}
```

---

## 📚 Resources for AI Implementation

### Enfusion Engine Documentation
- Official Docs: https://reforger.armaplatform.com/dev-hub
- EnfusionDatabaseFramework: https://github.com/Arkensor/EnfusionDatabaseFramework
- Community Wiki: https://community.bistudio.com/wiki/Arma_Reforger

### Modding Tutorials
- Workshop Tools Overview: YouTube "Arma Reforger Modding Boot Camp"
- Scripting Reference: Enfusion Workbench built-in docs
- Networking/Replication: Search Dev Hub for "replication tutorial"

### Middleware Options
- Node.js + Express: https://expressjs.com
- Python + Flask: https://flask.palletsprojects.com
- Go + Gin: https://gin-gonic.com

---

## 🎯 Success Criteria

The system is considered **fully functional** when:

1. ✅ Desktop app compiles and runs on Windows 10/11
2. ✅ Android app compiles and runs on Android 8+
3. ✅ Apps sync markers between each other via WebSocket
4. ✅ Game server mod is published to Workshop
5. ✅ Apps can send markers to game server
6. ✅ In-game players see markers placed from apps
7. ✅ Markers placed in-game appear in apps
8. ✅ System handles 20+ concurrent users
9. ✅ Latency < 2 seconds for marker sync
10. ✅ No data loss during disconnections

---

## 📞 Contact & Support

- **Project Lead**: [Your Name]
- **Discord**: https://discord.gg/ykkkjwDnAD
- **GitHub**: [Repository URL]
- **Documentation**: This file + code comments

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

**Note to AI Assistant**: This document provides the complete production architecture for the Arma Reforger Tactical Map System. Your task is to develop the Arma Reforger Workshop mod that bridges the desktop/mobile applications with the game server. Focus on creating a robust, performant solution using Enfusion scripting or a middleware approach as described above.

The desktop and mobile apps are being developed separately and will be ready for integration testing. Please refer to the API specifications and data formats in this document when implementing the mod.

**Key Files to Reference:**
- Desktop app source: `/app/electron_app/`
- Android app source: `/app/android_app/`
- Server configuration: 192.168.2.26 (ports 2001, 17777, 19999)
- Marker JSON schema: See "Data Format" section above

Good luck with the mod development! 🎮
