from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QLabel, QLineEdit, QPushButton, QCheckBox,
                                QMessageBox, QGroupBox, QComboBox, QDialog,
                                QDialogButtonBox, QGridLayout)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from gui.styles import DARK_THEME
import uuid


class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Account")
        self.setMinimumWidth(400)
        self.setStyleSheet(DARK_THEME)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)
        
        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        # Confirm Password
        layout.addWidget(QLabel("Confirm Password:"))
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_input)
        
        # Security Questions
        security_group = QGroupBox("Security Questions (for password reset)")
        security_layout = QVBoxLayout()
        
        security_layout.addWidget(QLabel("Question 1:"))
        self.q1_combo = QComboBox()
        self.q1_combo.addItems([
            "What was your first pet's name?",
            "What city were you born in?",
            "What is your mother's maiden name?",
            "What was the name of your first school?"
        ])
        security_layout.addWidget(self.q1_combo)
        
        security_layout.addWidget(QLabel("Answer 1:"))
        self.a1_input = QLineEdit()
        security_layout.addWidget(self.a1_input)
        
        security_layout.addWidget(QLabel("Question 2:"))
        self.q2_combo = QComboBox()
        self.q2_combo.addItems([
            "What is your favorite color?",
            "What was your childhood nickname?",
            "What is your favorite food?",
            "What was your first car?"
        ])
        security_layout.addWidget(self.q2_combo)
        
        security_layout.addWidget(QLabel("Answer 2:"))
        self.a2_input = QLineEdit()
        security_layout.addWidget(self.a2_input)
        
        security_group.setLayout(security_layout)
        layout.addWidget(security_group)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def validate_and_accept(self):
        if not self.username_input.text().strip():
            QMessageBox.warning(self, "Error", "Username is required")
            return
        
        if len(self.password_input.text()) < 4:
            QMessageBox.warning(self, "Error", "Password must be at least 4 characters")
            return
        
        if self.password_input.text() != self.confirm_password_input.text():
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        
        if not self.a1_input.text().strip() or not self.a2_input.text().strip():
            QMessageBox.warning(self, "Error", "Please answer both security questions")
            return
        
        self.accept()
    
    def get_data(self):
        return {
            'username': self.username_input.text().strip(),
            'password': self.password_input.text(),
            'security_q1': self.q1_combo.currentText(),
            'security_a1': self.a1_input.text().strip(),
            'security_q2': self.q2_combo.currentText(),
            'security_a2': self.a2_input.text().strip()
        }


class PasswordResetDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Password Reset")
        self.setMinimumWidth(400)
        self.setStyleSheet(DARK_THEME)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)
        
        self.verify_button = QPushButton("Verify Identity")
        self.verify_button.clicked.connect(self.verify_identity)
        layout.addWidget(self.verify_button)
        
        self.questions_widget = QWidget()
        self.questions_layout = QVBoxLayout()
        
        self.q1_label = QLabel()
        self.questions_layout.addWidget(self.q1_label)
        self.a1_input = QLineEdit()
        self.questions_layout.addWidget(self.a1_input)
        
        self.q2_label = QLabel()
        self.questions_layout.addWidget(self.q2_label)
        self.a2_input = QLineEdit()
        self.questions_layout.addWidget(self.a2_input)
        
        self.questions_layout.addWidget(QLabel("New Password:"))
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.questions_layout.addWidget(self.new_password_input)
        
        self.questions_widget.setLayout(self.questions_layout)
        self.questions_widget.setVisible(False)
        layout.addWidget(self.questions_widget)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.reset_password)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def verify_identity(self):
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Error", "Please enter username")
            return
        
        user = self.db.get_user_by_username(username)
        if not user:
            QMessageBox.warning(self, "Error", "User not found")
            return
        
        self.q1_label.setText(user[3])
        self.q2_label.setText(user[5])
        self.questions_widget.setVisible(True)
        self.verify_button.setEnabled(False)
    
    def reset_password(self):
        username = self.username_input.text().strip()
        
        if not self.questions_widget.isVisible():
            QMessageBox.warning(self, "Error", "Please verify your identity first")
            return
        
        if self.db.verify_security_answers(username, self.a1_input.text(), self.a2_input.text()):
            if len(self.new_password_input.text()) < 4:
                QMessageBox.warning(self, "Error", "Password must be at least 4 characters")
                return
            
            self.db.reset_password(username, self.new_password_input.text())
            QMessageBox.information(self, "Success", "Password reset successful!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Security answers are incorrect")


class LoginWindow(QMainWindow):
    login_successful = Signal(int, str, str)
    
    def __init__(self, db, device_id):
        super().__init__()
        self.db = db
        self.device_id = device_id
        self.setWindowTitle("Arma Reforger - Live Map Login")
        self.setMinimumSize(500, 400)
        self.setStyleSheet(DARK_THEME)
        self.setup_ui()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Title
        title = QLabel("ARMA REFORGER")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24pt; font-weight: bold; color: #5a7a51; margin-bottom: 10px;")
        layout.addWidget(title)
        
        subtitle = QLabel("Live Interactive Map")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14pt; color: #808080; margin-bottom: 30px;")
        layout.addWidget(subtitle)
        
        # Login form
        form_widget = QWidget()
        form_layout = QVBoxLayout()
        
        form_layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        form_layout.addWidget(self.username_input)
        
        form_layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.returnPressed.connect(self.handle_login)
        form_layout.addWidget(self.password_input)
        
        self.keep_logged_in = QCheckBox("Keep me logged in for 60 days")
        form_layout.addWidget(self.keep_logged_in)
        
        form_widget.setLayout(form_layout)
        layout.addWidget(form_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_button)
        
        self.register_button = QPushButton("Create Account")
        self.register_button.clicked.connect(self.show_register)
        button_layout.addWidget(self.register_button)
        
        layout.addLayout(button_layout)
        
        # Reset password link
        self.reset_link = QPushButton("Forgot Password?")
        self.reset_link.setStyleSheet("QPushButton { background: transparent; color: #5a7a51; text-decoration: underline; border: none; }")
        self.reset_link.clicked.connect(self.show_password_reset)
        layout.addWidget(self.reset_link, alignment=Qt.AlignCenter)
        
        layout.addStretch()
        central_widget.setLayout(layout)
    
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return
        
        user_id = self.db.verify_login(username, password)
        if user_id:
            keep_logged_in = self.keep_logged_in.isChecked()
            session_token = self.db.create_session(user_id, self.device_id, keep_logged_in)
            
            self.login_successful.emit(user_id, username, session_token)
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")
    
    def show_register(self):
        dialog = RegisterDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            user_id = self.db.create_user(
                data['username'],
                data['password'],
                data['security_q1'],
                data['security_a1'],
                data['security_q2'],
                data['security_a2']
            )
            
            if user_id:
                QMessageBox.information(self, "Success", "Account created successfully! You can now login.")
            else:
                QMessageBox.warning(self, "Error", "Username already exists")
    
    def show_password_reset(self):
        dialog = PasswordResetDialog(self.db, self)
        dialog.exec()
