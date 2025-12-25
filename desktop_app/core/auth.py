import pyotp
import qrcode
from io import BytesIO
from PyQt5.QtGui import QPixmap
from core.database import Database


class AuthManager:
    def __init__(self, db: Database):
        self.db = db
    
    def generate_totp_secret(self):
        """Generate a new TOTP secret"""
        return pyotp.random_base32()
    
    def generate_qr_code(self, username, secret):
        """Generate QR code for TOTP setup"""
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(name=username, issuer_name='Arma Reforger Map')
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to QPixmap
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.read())
        
        return pixmap, secret
    
    def verify_totp(self, secret, token):
        """Verify TOTP token"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)
    
    def setup_totp_for_user(self, user_id, username):
        """Setup TOTP for a user"""
        secret = self.generate_totp_secret()
        qr_pixmap, _ = self.generate_qr_code(username, secret)
        return qr_pixmap, secret
