import sys
import os
import uuid
import threading
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer
from gui.login_window import LoginWindow
from gui.main_window import MainWindow
from core.database import Database
from core.auth import AuthManager
from core.server_manager import ServerManager
from core.websocket_server import WebSocketServer

# Version information
VERSION = "0.099.021"
PREVIOUS_VERSION = "0.096.014"


class ArmaMapApplication:
    def __init__(self):
        # Get application path
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            self.app_path = os.path.dirname(sys.executable)
        else:
            # Running as script
            self.app_path = os.path.dirname(os.path.abspath(__file__))
        
        # Initialize components
        self.db = Database(self.app_path)
        self.auth_manager = AuthManager(self.db)
        
        config_path = os.path.join(self.app_path, 'config', 'servers.json')
        self.server_manager = ServerManager(config_path)
        
        # Get or create device ID
        self.device_id = self.get_or_create_device_id()
        
        # Start WebSocket server in background thread
        self.ws_server = WebSocketServer('localhost', self.server_manager.websocket_port)
        self.ws_thread = threading.Thread(target=self.ws_server.run, daemon=True)
        self.ws_thread.start()
        
        # Initialize Qt Application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Arma Reforger Live Map")
        
        # Check for existing session
        self.main_window = None
        self.login_window = None
        
    def get_or_create_device_id(self):
        """Get or create unique device ID"""
        device_id_file = os.path.join(self.app_path, 'data', '.device_id')
        os.makedirs(os.path.dirname(device_id_file), exist_ok=True)
        
        if os.path.exists(device_id_file):
            with open(device_id_file, 'r') as f:
                return f.read().strip()
        else:
            device_id = str(uuid.uuid4())
            with open(device_id_file, 'w') as f:
                f.write(device_id)
            return device_id
    
    def check_existing_session(self):
        """Check if there's a valid existing session"""
        session_file = os.path.join(self.app_path, 'data', '.session')
        if os.path.exists(session_file):
            try:
                with open(session_file, 'r') as f:
                    session_token = f.read().strip()
                
                user_id = self.db.verify_session(session_token, self.device_id)
                if user_id:
                    # Get username
                    import sqlite3
                    conn = sqlite3.connect(self.db.db_path)
                    cursor = conn.cursor()
                    cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
                    result = cursor.fetchone()
                    conn.close()
                    
                    if result:
                        return user_id, result[0], session_token
            except Exception as e:
                print(f"Session check error: {e}")
        
        return None, None, None
    
    def save_session(self, session_token):
        """Save session token to file"""
        session_file = os.path.join(self.app_path, 'data', '.session')
        with open(session_file, 'w') as f:
            f.write(session_token)
    
    def on_login_successful(self, user_id, username, session_token):
        """Handle successful login"""
        self.save_session(session_token)
        self.show_main_window(user_id, username, session_token)
    
    def show_main_window(self, user_id, username, session_token):
        """Show main map window"""
        self.main_window = MainWindow(
            self.db,
            self.auth_manager,
            self.server_manager,
            user_id,
            username,
            session_token
        )
        self.main_window.show()
    
    def run(self):
        """Run the application"""
        # Check for existing session
        user_id, username, session_token = self.check_existing_session()
        
        if user_id and username and session_token:
            # Valid session exists, go straight to main window
            self.show_main_window(user_id, username, session_token)
        else:
            # Show login window
            self.login_window = LoginWindow(self.db, self.device_id)
            self.login_window.login_successful.connect(self.on_login_successful)
            self.login_window.show()
        
        # Run application
        sys.exit(self.app.exec())


if __name__ == '__main__':
    app = ArmaMapApplication()
    app.run()
