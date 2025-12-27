import sqlite3
import os
import json
from datetime import datetime, timedelta
from core.encryption import EncryptionManager


class Database:
    def __init__(self, app_path):
        self.app_path = app_path
        self.db_path = os.path.join(app_path, 'data', 'arma_map.db')
        self.encryption = EncryptionManager(app_path)
        self._init_database()
    
    def _init_database(self):
        """Initialize database with required tables"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                security_q1 TEXT NOT NULL,
                security_a1 TEXT NOT NULL,
                security_q2 TEXT NOT NULL,
                security_a2 TEXT NOT NULL,
                totp_secret TEXT,
                totp_enabled INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                device_id TEXT NOT NULL,
                token TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Markers table (for persistent markers)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS markers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                marker_type TEXT NOT NULL,
                x REAL NOT NULL,
                y REAL NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username, password, security_q1, security_a1, security_q2, security_a2):
        """Create new user account"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            password_hash = self.encryption.hash_password(password)
            encrypted_a1 = self.encryption.encrypt(security_a1.lower())
            encrypted_a2 = self.encryption.encrypt(security_a2.lower())
            
            cursor.execute('''
                INSERT INTO users (username, password_hash, security_q1, security_a1, security_q2, security_a2, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, password_hash, security_q1, encrypted_a1, security_q2, encrypted_a2, datetime.now().isoformat()))
            
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            if conn:
                conn.close()
    
    def verify_login(self, username, password):
        """Verify user login credentials"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            
            if result and self.encryption.verify_password(password, result[1]):
                return result[0]
            return None
        finally:
            if conn:
                conn.close()
    
    def get_user_by_username(self, username):
        """Get user details by username"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            return result
        finally:
            if conn:
                conn.close()
    
    def verify_security_answers(self, username, answer1, answer2):
        """Verify security question answers"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            cursor.execute('SELECT security_a1, security_a2 FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            
            if result:
                decrypted_a1 = self.encryption.decrypt(result[0])
                decrypted_a2 = self.encryption.decrypt(result[1])
                return (decrypted_a1 == answer1.lower() and decrypted_a2 == answer2.lower())
            return False
        finally:
            if conn:
                conn.close()
    
    def reset_password(self, username, new_password):
        """Reset user password"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            password_hash = self.encryption.hash_password(new_password)
            cursor.execute('UPDATE users SET password_hash = ? WHERE username = ?', (password_hash, username))
            
            conn.commit()
        finally:
            if conn:
                conn.close()
    
    def create_session(self, user_id, device_id, keep_logged_in=False):
        """Create new session token"""
        import secrets
        
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(days=60 if keep_logged_in else 1)
            
            cursor.execute('''
                INSERT INTO sessions (user_id, device_id, token, expires_at)
                VALUES (?, ?, ?, ?)
            ''', (user_id, device_id, token, expires_at.isoformat()))
            
            conn.commit()
            return token
        finally:
            if conn:
                conn.close()
    
    def verify_session(self, token, device_id):
        """Verify session token"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, expires_at FROM sessions 
                WHERE token = ? AND device_id = ?
            ''', (token, device_id))
            result = cursor.fetchone()
            
            if result:
                expires_at = datetime.fromisoformat(result[1])
                if expires_at > datetime.now():
                    return result[0]
            return None
        finally:
            if conn:
                conn.close()
    
    def enable_totp(self, user_id, totp_secret):
        """Enable TOTP for user"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            encrypted_secret = self.encryption.encrypt(totp_secret)
            cursor.execute('UPDATE users SET totp_secret = ?, totp_enabled = 1 WHERE id = ?', 
                          (encrypted_secret, user_id))
            
            conn.commit()
        finally:
            if conn:
                conn.close()
    
    def get_totp_secret(self, user_id):
        """Get TOTP secret for user"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            cursor.execute('SELECT totp_secret, totp_enabled FROM users WHERE id = ?', (user_id,))
            result = cursor.fetchone()
            
            if result and result[1] == 1:
                return self.encryption.decrypt(result[0])
            return None
        finally:
            if conn:
                conn.close()
