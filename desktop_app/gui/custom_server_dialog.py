from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                                QLabel, QLineEdit, QPushButton, 
                                QDialogButtonBox, QMessageBox)
from PySide6.QtCore import Qt
from gui.styles import DARK_THEME
import re


class CustomServerDialog(QDialog):
    """Dialog for quickly adding a custom server by IP and Port"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.server_ip = ""
        self.server_port = 0
        self.server_name = ""
        
        self.setWindowTitle("Connect to Custom Server")
        self.setMinimumWidth(450)
        self.setStyleSheet(DARK_THEME)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title and instructions
        title = QLabel("Connect to ArmaLiveMap Server")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; color: #5a7a51;")
        layout.addWidget(title)
        
        instructions = QLabel(
            "Enter the server IP address and port to connect to ArmaLiveMap.\n"
            "If you know the server's IP, you can view the live map for that server."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #a0a0a0; margin-bottom: 10px;")
        layout.addWidget(instructions)
        
        # Server Name
        layout.addWidget(QLabel("Server Name (Optional):"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., My Favorite Server")
        layout.addWidget(self.name_input)
        
        # IP Address
        layout.addWidget(QLabel("Server IP Address:"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("e.g., 192.168.1.100 or server.example.com")
        layout.addWidget(self.ip_input)
        
        # Port Number
        layout.addWidget(QLabel("Port Number:"))
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("e.g., 2302")
        self.port_input.setText("2302")  # Default Arma Reforger port
        layout.addWidget(self.port_input)
        
        # Save option
        from PySide6.QtWidgets import QCheckBox
        self.save_checkbox = QCheckBox("Save this server to my server list")
        self.save_checkbox.setChecked(True)
        layout.addWidget(self.save_checkbox)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def validate_and_accept(self):
        """Validate inputs before accepting"""
        ip = self.ip_input.text().strip()
        port_text = self.port_input.text().strip()
        name = self.name_input.text().strip()
        
        # Validate IP
        if not ip:
            QMessageBox.warning(self, "Validation Error", "Please enter a server IP address.")
            return
        
        # Basic IP/hostname validation
        if not self.is_valid_ip_or_hostname(ip):
            QMessageBox.warning(self, "Validation Error", 
                              "Invalid IP address or hostname format.\n"
                              "Examples:\n"
                              "  192.168.1.100\n"
                              "  server.example.com")
            return
        
        # Validate Port
        try:
            port = int(port_text)
            if port < 1 or port > 65535:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Validation Error", 
                              "Port must be a number between 1 and 65535.")
            return
        
        # Set values
        self.server_ip = ip
        self.server_port = port
        self.server_name = name if name else f"{ip}:{port}"
        
        self.accept()
    
    def is_valid_ip_or_hostname(self, address):
        """Validate IP address or hostname"""
        # Check if it's a valid IP address
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ip_pattern, address):
            # Validate each octet is 0-255
            octets = address.split('.')
            return all(0 <= int(octet) <= 255 for octet in octets)
        
        # Check if it's a valid hostname/domain
        hostname_pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$'
        return bool(re.match(hostname_pattern, address))
    
    def get_server_info(self):
        """Return server information"""
        return {
            'name': self.server_name,
            'ip': self.server_ip,
            'port': self.server_port,
            'save': self.save_checkbox.isChecked()
        }
