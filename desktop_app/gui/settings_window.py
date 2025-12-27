from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QPushButton, QLabel, QDialog, QLineEdit,
                                QDialogButtonBox, QMessageBox, QGroupBox,
                                QComboBox, QCheckBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from gui.styles import DARK_THEME
from core.auth import AuthManager


class TOTPSetupDialog(QDialog):
    def __init__(self, qr_pixmap, secret, parent=None):
        super().__init__(parent)
        self.secret = secret
        self.setWindowTitle("Setup QR Code Authentication")
        self.setMinimumWidth(400)
        self.setStyleSheet(DARK_THEME)
        self.setup_ui(qr_pixmap)
    
    def setup_ui(self, qr_pixmap):
        layout = QVBoxLayout()
        
        instructions = QLabel(
            "1. Open your authenticator app (Google Authenticator, Authy, etc.)\n"
            "2. Scan the QR code below\n"
            "3. Enter the 6-digit code from your app to verify"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # QR Code
        qr_label = QLabel()
        qr_label.setPixmap(qr_pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(qr_label)
        
        # Secret key (manual entry)
        secret_label = QLabel(f"Manual Entry Key: {self.secret}")
        secret_label.setAlignment(Qt.AlignCenter)
        secret_label.setStyleSheet("color: #5a7a51; font-family: monospace;")
        layout.addWidget(secret_label)
        
        # Verification code input
        layout.addWidget(QLabel("Enter verification code:"))
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("000000")
        self.code_input.setMaxLength(6)
        layout.addWidget(self.code_input)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def get_code(self):
        return self.code_input.text().strip()


class TOTPVerifyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Authentication Code")
        self.setMinimumWidth(350)
        self.setStyleSheet(DARK_THEME)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Enter the 6-digit code from your authenticator app:"))
        
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("000000")
        self.code_input.setMaxLength(6)
        self.code_input.setAlignment(Qt.AlignCenter)
        self.code_input.setStyleSheet("font-size: 18pt; letter-spacing: 5px;")
        layout.addWidget(self.code_input)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def get_code(self):
        return self.code_input.text().strip()


class SettingsWindow(QDialog):
    def __init__(self, db, auth_manager, user_id, username, server_manager, parent=None):
        super().__init__(parent)
        self.db = db
        self.auth_manager = auth_manager
        self.user_id = user_id
        self.username = username
        self.server_manager = server_manager
        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 500)
        self.setStyleSheet(DARK_THEME)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Authentication Section
        auth_group = QGroupBox("QR Code Authentication (TOTP)")
        auth_layout = QVBoxLayout()
        
        totp_secret = self.db.get_totp_secret(self.user_id)
        
        if totp_secret:
            status_label = QLabel("✓ QR Code authentication is enabled")
            status_label.setStyleSheet("color: #5a7a51;")
            auth_layout.addWidget(status_label)
            
            disable_button = QPushButton("Disable QR Authentication")
            disable_button.clicked.connect(self.disable_totp)
            auth_layout.addWidget(disable_button)
        else:
            status_label = QLabel("QR Code authentication is not enabled")
            status_label.setStyleSheet("color: #808080;")
            auth_layout.addWidget(status_label)
            
            enable_button = QPushButton("Enable QR Authentication")
            enable_button.clicked.connect(self.enable_totp)
            auth_layout.addWidget(enable_button)
        
        auth_group.setLayout(auth_layout)
        layout.addWidget(auth_group)
        
        # Server Management Section
        server_group = QGroupBox("Server Configuration")
        server_layout = QVBoxLayout()
        
        server_layout.addWidget(QLabel("Configure up to 6 servers:"))
        
        for i in range(6):
            server = self.server_manager.servers[i]
            server_widget = self.create_server_widget(server)
            server_layout.addWidget(server_widget)
        
        save_servers_button = QPushButton("Save Server Configuration")
        save_servers_button.clicked.connect(self.save_servers)
        server_layout.addWidget(save_servers_button)
        
        server_group.setLayout(server_layout)
        layout.addWidget(server_group)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
    
    def create_server_widget(self, server):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 5, 0, 5)
        
        enabled_check = QCheckBox(f"Server {server['id']}")
        enabled_check.setChecked(server.get('enabled', False))
        enabled_check.setObjectName(f"enabled_{server['id']}")
        layout.addWidget(enabled_check)
        
        name_input = QLineEdit(server.get('name', ''))
        name_input.setPlaceholderText("Server Name")
        name_input.setObjectName(f"name_{server['id']}")
        layout.addWidget(name_input)
        
        ip_input = QLineEdit(server.get('ip', ''))
        ip_input.setPlaceholderText("IP Address")
        ip_input.setObjectName(f"ip_{server['id']}")
        layout.addWidget(ip_input)
        
        port_input = QLineEdit(str(server.get('port', '')))
        port_input.setPlaceholderText("Port")
        port_input.setMaximumWidth(100)
        port_input.setObjectName(f"port_{server['id']}")
        layout.addWidget(port_input)
        
        widget.setLayout(layout)
        return widget
    
    def save_servers(self):
        for i in range(1, 7):
            enabled_check = self.findChild(QCheckBox, f"enabled_{i}")
            name_input = self.findChild(QLineEdit, f"name_{i}")
            ip_input = self.findChild(QLineEdit, f"ip_{i}")
            port_input = self.findChild(QLineEdit, f"port_{i}")
            
            if enabled_check and name_input and ip_input and port_input:
                try:
                    port = int(port_input.text()) if port_input.text() else 0
                except ValueError:
                    port = 0
                
                self.server_manager.update_server(
                    i,
                    name_input.text(),
                    ip_input.text(),
                    port,
                    enabled_check.isChecked()
                )
        
        QMessageBox.information(self, "Success", "Server configuration saved!")
    
    def enable_totp(self):
        qr_pixmap, secret = self.auth_manager.setup_totp_for_user(self.user_id, self.username)
        
        dialog = TOTPSetupDialog(qr_pixmap, secret, self)
        if dialog.exec():
            code = dialog.get_code()
            if self.auth_manager.verify_totp(secret, code):
                self.db.enable_totp(self.user_id, secret)
                QMessageBox.information(self, "Success", "QR Code authentication enabled successfully!")
                self.accept()
                # Reopen settings to show updated status
                new_settings = SettingsWindow(self.db, self.auth_manager, self.user_id, 
                                             self.username, self.server_manager, self.parent())
                new_settings.exec()
            else:
                QMessageBox.warning(self, "Error", "Invalid verification code")
    
    def disable_totp(self):
        reply = QMessageBox.question(self, "Confirm", 
                                    "Are you sure you want to disable QR Code authentication?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Use database method for proper connection management
            conn = None
            try:
                import sqlite3
                conn = sqlite3.connect(self.db.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET totp_enabled = 0 WHERE id = ?', (self.user_id,))
                conn.commit()
                
                QMessageBox.information(self, "Success", "QR Code authentication disabled")
                self.accept()
                # Reopen settings
                new_settings = SettingsWindow(self.db, self.auth_manager, self.user_id,
                                             self.username, self.server_manager, self.parent())
                new_settings.exec()
            finally:
                if conn:
                    conn.close()
