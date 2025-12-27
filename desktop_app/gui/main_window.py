from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QPushButton, QLabel, QComboBox, QToolBar,
                                QStatusBar, QMessageBox, QCheckBox, QGroupBox,
                                QScrollArea, QFrame)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QAction, QIcon
from gui.styles import DARK_THEME
from gui.settings_window import SettingsWindow, TOTPVerifyDialog
from gui.feedback_dialog import FeedbackDialog
from gui.custom_server_dialog import CustomServerDialog
from map.map_viewer import MapViewer, ARMA_MARKER_TYPES
import json
import asyncio
import websockets

# Version information
VERSION = "0.099.023"


class WebSocketClient(QThread):
    message_received = Signal(dict)
    connected = Signal()
    disconnected = Signal()
    
    def __init__(self, host='localhost', port=8765):
        super().__init__()
        self.host = host
        self.port = port
        self.running = False
        self.websocket = None
    
    def run(self):
        self.running = True
        asyncio.run(self.connect())
    
    async def connect(self):
        uri = f"ws://{self.host}:{self.port}"
        try:
            # Connect to WebSocket server
            self.websocket = await websockets.connect(uri)
            self.connected.emit()
            
            # Listen for messages
            while self.running:
                try:
                    message = await asyncio.wait_for(self.websocket.recv(), timeout=0.1)
                    data = json.loads(message)
                    self.message_received.emit(data)
                except asyncio.TimeoutError:
                    continue
                except websockets.exceptions.ConnectionClosed:
                    break
                except Exception as e:
                    print(f"Error receiving message: {e}")
                    break
        except Exception as e:
            print(f"WebSocket connection error: {e}")
        finally:
            if self.websocket:
                await self.websocket.close()
            self.disconnected.emit()
    
    def send_message(self, data):
        """Send message to WebSocket server"""
        if self.websocket and not self.websocket.closed:
            try:
                # Create new event loop for sending
                loop = asyncio.new_event_loop()
                loop.run_until_complete(self.websocket.send(json.dumps(data)))
                loop.close()
            except Exception as e:
                print(f"Error sending message: {e}")
    
    def stop(self):
        self.running = False


class MainWindow(QMainWindow):
    def __init__(self, db, auth_manager, server_manager, user_id, username, session_token):
        super().__init__()
        self.db = db
        self.auth_manager = auth_manager
        self.server_manager = server_manager
        self.user_id = user_id
        self.username = username
        self.session_token = session_token
        self.ws_client = None
        
        self.setWindowTitle(f"Arma Reforger - Live Map v{VERSION} [{username}]")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(DARK_THEME)
        
        # Check if TOTP is enabled
        self.check_totp_auth()
        
        self.setup_ui()
        self.setup_websocket()
    
    def check_totp_auth(self):
        """Check if TOTP is enabled and verify"""
        totp_secret = self.db.get_totp_secret(self.user_id)
        if totp_secret:
            dialog = TOTPVerifyDialog(self)
            if dialog.exec():
                code = dialog.get_code()
                if not self.auth_manager.verify_totp(totp_secret, code):
                    QMessageBox.critical(self, "Error", "Invalid authentication code")
                    self.close()
            else:
                self.close()
    
    def setup_ui(self):
        # Create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Server selector
        toolbar.addWidget(QLabel("Server: "))
        self.server_combo = QComboBox()
        self.update_server_list()
        self.server_combo.currentIndexChanged.connect(self.on_server_changed)
        toolbar.addWidget(self.server_combo)
        
        # Custom server button
        custom_server_button = QPushButton("+ Custom Server")
        custom_server_button.setStyleSheet("QPushButton { background-color: #3a5a36; }")
        custom_server_button.clicked.connect(self.show_custom_server_dialog)
        toolbar.addWidget(custom_server_button)
        
        toolbar.addSeparator()
        
        # Zoom controls
        toolbar.addWidget(QLabel("Zoom: "))
        zoom_in_button = QPushButton("+ Zoom In")
        zoom_in_button.clicked.connect(self.map_viewer.zoom_in)
        toolbar.addWidget(zoom_in_button)
        
        zoom_out_button = QPushButton("− Zoom Out")
        zoom_out_button.clicked.connect(self.map_viewer.zoom_out)
        toolbar.addWidget(zoom_out_button)
        
        reset_zoom_button = QPushButton("⟲ Reset")
        reset_zoom_button.clicked.connect(self.map_viewer.reset_zoom)
        toolbar.addWidget(reset_zoom_button)
        
        toolbar.addSeparator()
        
        # Marker type selector
        toolbar.addWidget(QLabel("Marker Type: "))
        self.marker_type_combo = QComboBox()
        for marker_key, marker_data in ARMA_MARKER_TYPES.items():
            self.marker_type_combo.addItem(marker_data['name'], marker_key)
        self.marker_type_combo.currentIndexChanged.connect(self.on_marker_type_changed)
        toolbar.addWidget(self.marker_type_combo)
        
        toolbar.addSeparator()
        
        # Clear markers button
        clear_button = QPushButton("Clear My Markers")
        clear_button.clicked.connect(self.clear_my_markers)
        toolbar.addWidget(clear_button)
        
        toolbar.addSeparator()
        
        # Feedback button
        feedback_button = QPushButton("📝 Feedback")
        feedback_button.clicked.connect(self.show_feedback)
        feedback_button.setStyleSheet("QPushButton { background-color: #4a5a46; }")
        toolbar.addWidget(feedback_button)
        
        # Settings button
        settings_button = QPushButton("⚙ Settings")
        settings_button.clicked.connect(self.show_settings)
        toolbar.addWidget(settings_button)
        
        # Refresh button
        refresh_button = QPushButton("↻ Refresh")
        refresh_button.clicked.connect(self.refresh_connection)
        toolbar.addWidget(refresh_button)
        
        # Main widget with sidebar
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout()
        
        # Map viewer (main area)
        map_layout = QVBoxLayout()
        self.map_viewer = MapViewer(self.user_id)
        self.map_viewer.marker_added.connect(self.on_marker_added)
        self.map_viewer.marker_removed.connect(self.on_marker_removed)
        map_layout.addWidget(self.map_viewer)
        
        # Info bar
        info_layout = QHBoxLayout()
        self.connection_status = QLabel("❌ Not Connected")
        self.connection_status.setStyleSheet("color: #ff5555;")
        info_layout.addWidget(self.connection_status)
        
        info_layout.addStretch()
        
        zoom_info = QLabel("Tip: Hold Ctrl + Mouse Wheel to zoom")
        zoom_info.setStyleSheet("color: #808080; font-size: 9pt;")
        info_layout.addWidget(zoom_info)
        
        info_layout.addStretch()
        
        self.player_count = QLabel("Players: 0")
        info_layout.addWidget(self.player_count)
        
        map_layout.addLayout(info_layout)
        
        main_layout.addLayout(map_layout, stretch=4)
        
        # Sidebar for filters
        sidebar = self.create_filter_sidebar()
        main_layout.addWidget(sidebar, stretch=1)
        
        main_widget.setLayout(main_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"Logged in as {self.username} | Version {VERSION}")
    
    def create_filter_sidebar(self):
        """Create sidebar with marker filters"""
        sidebar_widget = QFrame()
        sidebar_widget.setFrameShape(QFrame.StyledPanel)
        sidebar_widget.setStyleSheet("QFrame { background-color: #1a1a1a; border-left: 2px solid #3a3a3a; }")
        sidebar_widget.setMaximumWidth(250)
        
        sidebar_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Marker Filters")
        title.setStyleSheet("font-size: 12pt; font-weight: bold; color: #5a7a51; padding: 10px;")
        sidebar_layout.addWidget(title)
        
        # Scroll area for filters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        filter_widget = QWidget()
        filter_layout = QVBoxLayout()
        
        self.filter_checkboxes = {}
        
        for marker_key, marker_data in ARMA_MARKER_TYPES.items():
            checkbox = QCheckBox(marker_data['name'])
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(lambda state, mk=marker_key: self.on_filter_changed(mk, state))
            filter_layout.addWidget(checkbox)
            self.filter_checkboxes[marker_key] = checkbox
        
        filter_layout.addStretch()
        filter_widget.setLayout(filter_layout)
        scroll.setWidget(filter_widget)
        
        sidebar_layout.addWidget(scroll)
        
        # Select/Deselect all buttons
        button_layout = QHBoxLayout()
        select_all_btn = QPushButton("All")
        select_all_btn.clicked.connect(self.select_all_filters)
        button_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("None")
        deselect_all_btn.clicked.connect(self.deselect_all_filters)
        button_layout.addWidget(deselect_all_btn)
        
        sidebar_layout.addLayout(button_layout)
        
        sidebar_widget.setLayout(sidebar_layout)
        return sidebar_widget
    
    def on_filter_changed(self, marker_type, state):
        """Handle filter checkbox state change"""
        visible = (state == Qt.Checked)
        self.map_viewer.set_marker_filter(marker_type, visible)
    
    def select_all_filters(self):
        """Select all marker filters"""
        for checkbox in self.filter_checkboxes.values():
            checkbox.setChecked(True)
    
    def deselect_all_filters(self):
        """Deselect all marker filters"""
        for checkbox in self.filter_checkboxes.values():
            checkbox.setChecked(False)
    
    def update_server_list(self):
        """Update server dropdown with enabled servers"""
        self.server_combo.clear()
        enabled_servers = self.server_manager.get_enabled_servers()
        
        if not enabled_servers:
            self.server_combo.addItem("No servers configured")
            return
        
        for server in enabled_servers:
            self.server_combo.addItem(f"{server['name']} ({server['ip']}:{server['port']})", server['id'])
    
    def setup_websocket(self):
        """Setup WebSocket connection"""
        self.ws_client = WebSocketClient('localhost', self.server_manager.websocket_port)
        self.ws_client.message_received.connect(self.on_websocket_message)
        self.ws_client.connected.connect(self.on_websocket_connected)
        self.ws_client.disconnected.connect(self.on_websocket_disconnected)
        self.ws_client.start()
    
    def on_websocket_connected(self):
        self.connection_status.setText("✓ Connected")
        self.connection_status.setStyleSheet("color: #5a7a51;")
    
    def on_websocket_disconnected(self):
        self.connection_status.setText("❌ Disconnected")
        self.connection_status.setStyleSheet("color: #ff5555;")
    
    def on_websocket_message(self, data):
        """Handle incoming WebSocket messages"""
        if data['type'] == 'marker_added':
            marker_data = data['marker']
            from map.map_viewer import MapMarker
            marker = MapMarker(
                marker_data['id'],
                marker_data['type'],
                marker_data['x'],
                marker_data['y'],
                marker_data['user_id'],
                marker_data.get('description', '')
            )
            self.map_viewer.add_marker_visual(marker)
        
        elif data['type'] == 'marker_removed':
            self.map_viewer.remove_marker(data['marker_id'])
        
        elif data['type'] == 'markers_sync':
            # Sync all markers when connecting
            for marker_data in data['markers']:
                from map.map_viewer import MapMarker
                marker = MapMarker(
                    marker_data['id'],
                    marker_data['type'],
                    marker_data['x'],
                    marker_data['y'],
                    marker_data['user_id'],
                    marker_data.get('description', '')
                )
                self.map_viewer.add_marker_visual(marker)
    
    def on_marker_added(self, marker):
        """Send marker to server"""
        if self.ws_client:
            message = {
                'type': 'marker_add',
                'marker': {
                    'type': marker.type,
                    'x': marker.x,
                    'y': marker.y,
                    'user_id': marker.user_id,
                    'description': marker.description,
                    'timestamp': marker.timestamp
                }
            }
            self.ws_client.send_message(message)
    
    def on_marker_removed(self, marker_id):
        """Send marker removal to server"""
        if self.ws_client:
            message = {
                'type': 'marker_remove',
                'marker_id': marker_id
            }
            self.ws_client.send_message(message)
    
    def on_server_changed(self, index):
        """Handle server selection change"""
        if index >= 0:
            self.status_bar.showMessage(f"Connected to: {self.server_combo.currentText()}")
    
    def on_marker_type_changed(self, index):
        """Handle marker type change"""
        marker_key = self.marker_type_combo.itemData(index)
        if marker_key:
            self.map_viewer.set_marker_mode(marker_key)
    
    def clear_my_markers(self):
        """Clear all markers placed by current user"""
        markers_to_remove = []
        for marker_id, marker_data in self.map_viewer.markers.items():
            if marker_data['marker'].user_id == self.user_id:
                markers_to_remove.append(marker_id)
        
        for marker_id in markers_to_remove:
            self.map_viewer.remove_marker(marker_id)
    
    def show_settings(self):
        """Show settings dialog"""
        settings = SettingsWindow(self.db, self.auth_manager, self.user_id, 
                                 self.username, self.server_manager, self)
        settings.exec()
        # Refresh server list after settings close
        self.update_server_list()
    
    def show_feedback(self):
        """Show feedback dialog"""
        feedback = FeedbackDialog(self.user_id, self.username, self)
        feedback.exec()
    
    def show_custom_server_dialog(self):
        """Show dialog to add custom server"""
        dialog = CustomServerDialog(self)
        if dialog.exec():
            server_info = dialog.get_server_info()
            
            # Add to server manager if save option is checked
            if server_info['save']:
                server_id = self.server_manager.add_server(
                    server_info['name'],
                    server_info['ip'],
                    server_info['port'],
                    enabled=True
                )
                
                # Refresh server list
                self.update_server_list()
                
                # Select the newly added server
                for i in range(self.server_combo.count()):
                    if self.server_combo.itemData(i) == server_id:
                        self.server_combo.setCurrentIndex(i)
                        break
                
                self.status_bar.showMessage(
                    f"Server added: {server_info['name']} ({server_info['ip']}:{server_info['port']})"
                )
            else:
                # Temporary connection without saving
                self.status_bar.showMessage(
                    f"Connecting to: {server_info['name']} ({server_info['ip']}:{server_info['port']})"
                )
            
            # Show info message
            QMessageBox.information(
                self,
                "Server Connected",
                f"Now viewing map for:\n\n"
                f"Server: {server_info['name']}\n"
                f"IP: {server_info['ip']}\n"
                f"Port: {server_info['port']}\n\n"
                f"{'Server saved to your list.' if server_info['save'] else 'Temporary connection (not saved).'}"
            )
    
    def refresh_connection(self):
        """Refresh WebSocket connection"""
        if self.ws_client:
            self.ws_client.stop()
            self.ws_client.wait()
        self.setup_websocket()
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.ws_client:
            self.ws_client.stop()
            self.ws_client.wait()
        event.accept()
