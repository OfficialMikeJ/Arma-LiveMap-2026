# Version 0.099.021 - Feature Update Summary

## 🎉 What's New in Version 0.099.021

### Release Date: 2026 (Planned)
### Previous Version: 0.096.014

---

## 🆕 Major New Features

### 1. Map Zoom Controls ✨
**What:** Full zoom control for the tactical map

**How to Use:**
- Click **"+"** button in toolbar to zoom in
- Click **"−"** button in toolbar to zoom out  
- Click **"⟲ Reset"** to return to 100% zoom
- **Pro tip:** Hold **Ctrl** and scroll **Mouse Wheel** for precise zoom control

**Zoom Range:** 25% to 500%

---

### 2. Enhanced Map Scrolling 🗺️
**What:** Smooth panning across the entire map area

**Features:**
- Drag anywhere to pan the map
- Zoom anchors under mouse cursor (natural feel)
- Scroll bars for precise positioning
- Improved viewport management

---

### 3. Vanilla Arma Reforger Markers 🎯
**What:** Full support for all official Arma Reforger marker types

**13 Marker Types:**
| Type | Shape | Use Case |
|------|-------|----------|
| Enemy | Red Circle | Mark hostile forces |
| Friendly | Blue Circle | Mark allied units |
| Attack | Red Arrow | Indicate attack direction |
| Defend | Blue Square | Mark defensive positions |
| Pickup | Green Triangle ▲ | Extraction/pickup points |
| Drop | Red Triangle ▼ | Drop zones |
| Meet | Purple Star ★ | Rendezvous points |
| Infantry | Green Circle | Infantry units |
| Armor | Yellow Square | Armored vehicles |
| Air | Light Blue Triangle | Aircraft |
| Naval | Blue Diamond | Naval units |
| Objective | Yellow Diamond | Mission objectives |
| Other | Gray Circle | General purpose |

**Visual Features:**
- Different shapes for instant recognition
- Color-coded for quick identification
- Consistent with Arma Reforger's marker system
- White outline for visibility

---

### 4. Advanced Filter System 🔍
**What:** Show/hide markers by type for tactical clarity

**Features:**
- **Sidebar** with all marker types listed
- **Individual toggle** for each marker type
- **Real-time filtering** (instant show/hide)
- **Quick actions:** "All" and "None" buttons
- **Filter persistence** maintains your preferences

**Use Cases:**
- Hide friendly markers to focus on threats
- Show only objectives during mission planning
- Filter out clutter for specific operations
- Create custom views for different roles

---

### 5. Feedback System 📝
**What:** Built-in feedback and bug reporting

**Features:**
- **Submit Feedback** form right in the app
- **Bug reports** with detailed descriptions
- **Feature requests** to shape future development
- **Discord integration** button for community access
- **Optional email** for follow-up
- Local storage (admin dashboard coming later)

**How to Use:**
1. Click **"📝 Feedback"** in toolbar
2. Enter subject and detailed feedback
3. Optionally add your email
4. Click **"Submit Feedback"**
5. Join Discord community for updates

**Discord Community:** https://discord.gg/ykkkjwDnAD

---

## 📊 Feature Comparison

| Feature | v0.096.014 | v0.099.021 |
|---------|------------|------------|
| Zoom Controls | ❌ | ✅ Buttons + Ctrl+Wheel |
| Map Scrolling | Basic | ✅ Enhanced |
| Marker Types | 4 basic | ✅ 13 vanilla types |
| Marker Shapes | Circles only | ✅ 7 different shapes |
| Filter System | ❌ | ✅ Advanced sidebar |
| Feedback System | ❌ | ✅ Built-in form |
| Discord Integration | ❌ | ✅ Direct link |

---

## 🎮 Improved User Experience

### Before (v0.096.014)
- Fixed zoom level
- 4 basic marker types (all circles)
- No marker filtering
- No feedback mechanism

### After (v0.099.021)
- ✅ Adjustable zoom (25% - 500%)
- ✅ 13 specialized marker types
- ✅ 7 different marker shapes
- ✅ Real-time marker filtering
- ✅ Built-in feedback system
- ✅ Discord community access
- ✅ Better tooltips and hints

---

## 🔧 Technical Improvements

### Performance
- Improved marker rendering with shape caching
- Better filter application (O(1) lookup)
- Optimized zoom transformation
- Enhanced viewport management

### Code Quality
- Modular marker system with ARMA_MARKER_TYPES
- Cleaner filter management
- Better separation of concerns
- Improved event handling

### User Interface
- Professional filter sidebar
- Better toolbar organization
- Status bar with helpful tips
- Version number in title bar

---

## 💾 Data Storage (No Changes)

All data remains stored locally:
- ✅ User accounts and sessions
- ✅ Server configurations
- ✅ Security settings
- 🆕 Feedback submissions (new file: `data/feedback/feedback_submissions.json`)

**No internet transmission** - Complete privacy maintained

---

## 🚀 How to Update

### From v0.096.014 to v0.099.021

1. **Download** the new version from GitHub Actions
2. **Extract** to a new folder (keep old version as backup)
3. **Copy** your `data/` folder from old version (if you want to keep accounts)
4. **Run** the new `ArmaReforgerMap.exe`
5. **Enjoy** the new features!

**Note:** Your existing accounts, sessions, and server configurations will work seamlessly.

---

## 🐛 Known Issues

### Current Limitations
- Admin dashboard for feedback not yet implemented
- Feedback stored locally only
- Map image is still placeholder (custom maps coming later)
- No cloud sync yet (all local)

### Coming Soon
- Admin dashboard for centralized feedback
- Cloud sync option (optional)
- Real Arma Reforger map images
- Player position tracking from servers

---

## 📖 Documentation Updates

Updated documentation files:
- ✅ `README.md` - Complete feature list
- ✅ `CHANGELOG.md` - Version history
- ✅ `QUICKSTART.md` - Updated usage guide
- ✅ Version numbers in all docs

---

## 🙏 Thank You

Thank you to our community for:
- Beta testing
- Feature suggestions
- Bug reports
- Continued support

**Join our Discord** to be part of the development process!
https://discord.gg/ykkkjwDnAD

---

## 📅 Release Timeline

- **v0.096.014**: December 2025 (Released)
- **v0.099.021**: 2026 (This release)
- **v0.100.x**: TBD (Admin dashboard + more)
- **v1.0.0**: TBD (Full production release)

---

## 🎯 Quick Start with New Features

### After Installing v0.099.021:

1. **Try Zoom:**
   - Ctrl + Scroll Wheel to zoom
   - Click +/− buttons

2. **Explore Markers:**
   - Select different marker types from dropdown
   - Place various markers on map
   - See different shapes and colors

3. **Use Filters:**
   - Open the sidebar on the right
   - Toggle marker types on/off
   - Try "All" and "None" buttons

4. **Submit Feedback:**
   - Click 📝 Feedback button
   - Share your thoughts
   - Join Discord community

---

**Enjoy the enhanced tactical experience!** 🎮
