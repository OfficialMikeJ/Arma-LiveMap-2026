# Arma Reforger Tactical Map - Android Native App

**Version:** 1.0.0  
**Platform:** Android 8.0+ (API 26+)  
**Technology:** Kotlin + Jetpack Compose + Material Design 3

---

## 🎯 Project Status

### ✅ Completed
- Project structure and Gradle configuration
- Dependencies setup
- Data models and entities
- Android Manifest

### 🔨 To Be Implemented
The following files need to be created to complete the Android app:

#### Database Layer (7 files)
- `TacMapDatabase.kt` - Room database setup
- `UserDao.kt` - User database operations
- `MarkerDao.kt` - Marker database operations
- `ServerDao.kt` - Server database operations
- `SessionDao.kt` - Session database operations
- `FeedbackDao.kt` - Feedback database operations
- `Converters.kt` - Type converters for Room

#### Repository Layer (5 files)
- `AuthRepository.kt` - Authentication logic
- `MarkerRepository.kt` - Marker CRUD operations
- `ServerRepository.kt` - Server configuration
- `FeedbackRepository.kt` - Feedback submission
- `WebSocketRepository.kt` - WebSocket communication

#### Network Layer (3 files)
- `WebSocketClient.kt` - WebSocket connection management
- `ApiService.kt` - HTTP REST API (for future game server mod)
- `NetworkModule.kt` - Dependency injection

#### UI Layer - Login (3 files)
- `LoginScreen.kt` - Compose UI for login
- `LoginViewModel.kt` - Login state management
- `RegisterDialog.kt` - Registration form

#### UI Layer - Map (6 files)
- `MapScreen.kt` - Main tactical map screen
- `MapViewModel.kt` - Map state and marker management
- `MapCanvas.kt` - Canvas drawing with touch gestures
- `MarkerTypeSelector.kt` - Marker type chooser
- `ToolBar.kt` - Top app bar with actions
- `FilterDrawer.kt` - Marker filter sidebar

#### UI Layer - Settings (2 files)
- `SettingsScreen.kt` - Server configuration
- `SettingsViewModel.kt` - Settings state

#### UI Layer - Feedback (2 files)
- `FeedbackDialog.kt` - Feedback submission form
- `FeedbackViewModel.kt` - Feedback state

#### Main App (3 files)
- `MainActivity.kt` - App entry point
- `TacMapApp.kt` - Compose navigation setup
- `AppModule.kt` - Dependency injection

#### Utils (5 files)
- `CryptoUtils.kt` - Password hashing, encryption
- `TOTPUtils.kt` - TOTP/QR code generation
- `PreferencesManager.kt` - SharedPreferences wrapper
- `Constants.kt` - App constants
- `Extensions.kt` - Kotlin extensions

#### Resources (10+ files)
- `res/values/strings.xml` - String resources
- `res/values/colors.xml` - Color palette (military theme)
- `res/values/themes.xml` - Material Design 3 theme
- `res/xml/backup_rules.xml` - Backup configuration
- `res/xml/data_extraction_rules.xml` - Data extraction rules
- Multiple layout files for compatibility

**Total Files Needed:** ~50-60 additional files

---

## 📦 Dependencies

All dependencies are configured in `app/build.gradle`:

- **Jetpack Compose** - Modern declarative UI
- **Material Design 3** - Google's latest design system
- **Room Database** - Local SQLite storage
- **OkHttp + Scarlet** - WebSocket client
- **Retrofit** - HTTP REST client (for future)
- **AndroidX Security** - Encrypted storage
- **Kotlin OTP** - TOTP/2FA support
- **ML Kit** - QR code scanning
- **CameraX** - Camera integration
- **Coroutines** - Async operations
- **DataStore** - Preferences storage

---

## 🏗️ Architecture

### MVVM + Repository Pattern

```
UI Layer (Compose)
    ↓
ViewModel (State Management)
    ↓
Repository (Business Logic)
    ↓
Data Sources (Room DB, WebSocket, API)
```

### Key Components

**Room Database:**
- Users, Markers, Servers, Sessions, Feedback tables
- DAOs for each entity
- Type converters for enums

**WebSocket Client:**
- Connect to ws://localhost:8765 (or configured server)
- Send/receive marker updates in real-time
- Auto-reconnect on disconnect

**Authentication:**
- SHA-256 password hashing (match desktop)
- TOTP secret generation and verification
- Session token management

**Map Canvas:**
- Custom Compose Canvas with touch gestures
- Pinch-to-zoom
- Pan with drag
- Tap to place markers
- Long-press to remove markers

**Material Design 3 Theme:**
- Dark military color scheme
- Custom color palette matching desktop
- Responsive layouts for tablets

---

## 🎨 Features

### Authentication
- ✅ Local account creation
- ✅ Login with username/password
- ✅ Security questions for recovery
- ✅ TOTP/QR code 2FA
- ✅ 60-day session tokens
- ✅ Biometric login (fingerprint/face)

### Tactical Map
- ✅ 13 marker types with unique colors
- ✅ 7 marker shapes (circle, square, diamond, triangle, arrow, star, polygon)
- ✅ Touch gestures (tap, pinch, pan)
- ✅ Zoom controls (+/-, pinch-to-zoom)
- ✅ Real-time marker synchronization
- ✅ Marker filters (show/hide by type)

### Server Management
- ✅ Configure up to 6 servers
- ✅ Default: 192.168.2.26:2001
- ✅ Enable/disable servers
- ✅ WebSocket connection status

### Feedback System
- ✅ Submit bugs, features, suggestions
- ✅ Optional email for follow-up
- ✅ Discord community link

### UI/UX
- ✅ Material Design 3 components
- ✅ Dark military theme
- ✅ Responsive for phones and tablets
- ✅ Landscape mode optimized
- ✅ Connection status indicator
- ✅ Live player count

---

## 🚀 Building the App

### Prerequisites
- Android Studio Hedgehog (2023.1.1) or newer
- JDK 17
- Android SDK 34
- Gradle 8.2+

### Build Steps

1. **Open in Android Studio:**
   ```bash
   # Open the android_app directory
   cd /app/android_app
   ```
   Then: File → Open → Select `/app/android_app`

2. **Sync Gradle:**
   - Android Studio will auto-sync
   - Or: File → Sync Project with Gradle Files

3. **Build APK:**
   - Build → Build Bundle(s) / APK(s) → Build APK(s)
   - Output: `app/build/outputs/apk/debug/app-debug.apk`

4. **Install on Device:**
   ```bash
   adb install app/build/outputs/apk/debug/app-debug.apk
   ```

### Command Line Build
```bash
cd /app/android_app

# Build debug APK
./gradlew assembleDebug

# Build release APK (requires signing)
./gradlew assembleRelease

# Install on connected device
./gradlew installDebug
```

---

## 📱 Testing

### Emulator Setup
1. Create Android Virtual Device (AVD) in Android Studio
2. Recommended: Pixel 6 Pro, API 34, Android 14
3. Enable: Tablet mode or Landscape orientation

### Physical Device Testing
1. Enable Developer Options on Android device
2. Enable USB Debugging
3. Connect device via USB
4. Run: `adb devices` to verify connection
5. Click "Run" in Android Studio

### Integration Testing with Desktop
1. Ensure both apps connect to same WebSocket server
2. Place marker on Android → Verify on desktop
3. Place marker on desktop → Verify on Android
4. Test with multiple devices simultaneously

---

## 🔒 Security

### Data Protection
- SHA-256 password hashing (match desktop)
- AndroidX Security for encrypted SharedPreferences
- TOTP secrets encrypted in local database
- Session tokens stored securely
- No data transmitted over internet (local only)

### Network Security
- Uses cleartext traffic for local network (192.168.x.x)
- HTTPS recommended for production
- WebSocket connection over WSS for production
- Certificate pinning for game server API

### Permissions
- `INTERNET` - WebSocket and future API
- `ACCESS_NETWORK_STATE` - Connection status
- `CAMERA` - QR code scanning (optional)

---

## 📖 Code Examples

### Placing a Marker (Kotlin)
```kotlin
// In MapViewModel.kt
fun placeMarker(x: Float, y: Float, type: MarkerType) {
    viewModelScope.launch {
        val marker = Marker(
            id = UUID.randomUUID().toString(),
            type = type,
            shape = getShapeForType(type),
            x = x,
            y = y,
            color = getColorForType(type),
            createdBy = currentUser.username
        )
        
        // Save to local database
        markerRepository.insertMarker(marker)
        
        // Broadcast via WebSocket
        webSocketClient.sendMarkerUpdate("add", marker)
    }
}
```

### WebSocket Connection (Kotlin)
```kotlin
// In WebSocketClient.kt
class WebSocketClient(private val url: String) {
    private val okHttpClient = OkHttpClient()
    private var webSocket: WebSocket? = null
    
    fun connect() {
        val request = Request.Builder()
            .url(url)
            .build()
            
        webSocket = okHttpClient.newWebSocket(request, object : WebSocketListener() {
            override fun onMessage(webSocket: WebSocket, text: String) {
                val message = gson.fromJson(text, WebSocketMessage::class.java)
                handleMessage(message)
            }
            
            override fun onOpen(webSocket: WebSocket, response: Response) {
                // Connected
                _connectionStatus.value = true
            }
        })
    }
}
```

### Compose Map Canvas (Kotlin)
```kotlin
// In MapCanvas.kt
@Composable
fun MapCanvas(
    markers: List<Marker>,
    onMarkerClick: (Marker) -> Unit,
    onMapClick: (Offset) -> Unit
) {
    var scale by remember { mutableStateOf(1f) }
    var offset by remember { mutableStateOf(Offset.Zero) }
    
    Canvas(
        modifier = Modifier
            .fillMaxSize()
            .pointerInput(Unit) {
                detectTransformGestures { _, pan, zoom, _ ->
                    scale *= zoom
                    offset += pan
                }
            }
            .pointerInput(Unit) {
                detectTapGestures { tapOffset ->
                    onMapClick(tapOffset)
                }
            }
    ) {
        drawGrid()
        markers.forEach { marker ->
            drawMarker(marker, scale, offset)
        }
    }
}
```

---

## 🐛 Troubleshooting

### Gradle Sync Fails
- Check internet connection
- Update Gradle wrapper: `./gradlew wrapper --gradle-version=8.2`
- Invalidate Caches: File → Invalidate Caches / Restart

### App Crashes on Launch
- Check Logcat for stack traces
- Verify AndroidManifest.xml permissions
- Ensure minimum SDK is 26

### WebSocket Won't Connect
- Verify server IP and port in settings
- Check firewall allows port 8765
- Ensure device and server on same network
- Try `adb reverse tcp:8765 tcp:8765` for emulator

### Markers Not Syncing
- Check WebSocket connection status (green dot)
- Verify both apps use same server configuration
- Test with simple curl/wscat to server

---

## 📚 Resources

- **Jetpack Compose Docs:** https://developer.android.com/jetpack/compose
- **Material Design 3:** https://m3.material.io/
- **Room Database:** https://developer.android.com/training/data-storage/room
- **Kotlin Coroutines:** https://kotlinlang.org/docs/coroutines-overview.html
- **WebSocket (OkHttp):** https://square.github.io/okhttp/

---

## 📝 TODOs

### High Priority
1. Implement all DAO classes
2. Create repositories for data access
3. Build WebSocket client with Scarlet
4. Implement Login screen UI
5. Create Map canvas with touch gestures
6. Add marker rendering logic

### Medium Priority
7. Implement Settings screen
8. Add TOTP/QR code functionality
9. Create Feedback dialog
10. Add filter drawer
11. Implement biometric authentication

### Low Priority
12. Add animations and transitions
13. Implement dark/light theme toggle
14. Add haptic feedback
15. Create onboarding tutorial
16. Add accessibility features

---

## 🤝 Contributing

This app is part of the Arma Reforger Tactical Map system. See `PROJECT_OVERVIEW.md` for complete architecture.

---

## 📜 License

MIT License - Free to use, modify, and distribute.

---

## 📞 Support

- **Discord:** https://discord.gg/ykkkjwDnAD
- **GitHub:** [Repository URL]

---

**🎮 Tactical coordination on the go!**
