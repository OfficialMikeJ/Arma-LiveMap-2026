from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                QTextEdit, QPushButton, QMessageBox, QLineEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices, QIcon
from PySide6.QtCore import QUrl
from gui.styles import DARK_THEME
import json
import os
from datetime import datetime


class FeedbackDialog(QDialog):
    def __init__(self, user_id, username, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.username = username
        self.setWindowTitle("Submit Feedback")
        self.setMinimumSize(500, 450)
        self.setStyleSheet(DARK_THEME)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Feedback System")
        title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #5a7a51;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Help us improve the Arma Reforger Live Map")
        subtitle.setStyleSheet("font-size: 10pt; color: #808080;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Email field
        layout.addWidget(QLabel("Email (optional):"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("your.email@example.com")
        layout.addWidget(self.email_input)
        
        # Subject field
        layout.addWidget(QLabel("Subject:"))
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Brief description of your feedback")
        layout.addWidget(self.subject_input)
        
        # Feedback text area
        layout.addWidget(QLabel("Feedback:"))
        self.feedback_text = QTextEdit()
        self.feedback_text.setPlaceholderText(
            "Share your thoughts, report bugs, or suggest features...\\n\\n"
            "Examples:\\n"
            "- Bug: Markers not syncing properly\\n"
            "- Feature: Add voice chat support\\n"
            "- Improvement: Better map resolution"
        )
        self.feedback_text.setMinimumHeight(150)
        layout.addWidget(self.feedback_text)
        
        # Admin dashboard notice
        notice = QLabel(
            "All feedback is collected and used to analyze, conduct bug report fixes "
            "& helps improve our application development process."
        )
        notice.setStyleSheet("color: #808080; font-size: 9pt;")
        notice.setWordWrap(True)
        layout.addWidget(notice)
        
        layout.addSpacing(10)
        
        # Future implementation notice
        future_notice = QLabel(
            "This feature is not fully implemented and will be added in a near future update "
            "at a later time. Join our Discord to follow for updates, bug fixes and major "
            "improvements to our tools, software and applications."
        )
        future_notice.setStyleSheet("color: #5a7a51; font-size: 9pt; font-style: italic;")
        future_notice.setWordWrap(True)
        layout.addWidget(future_notice)
        
        layout.addSpacing(10)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Discord button
        self.discord_button = QPushButton("🎮 Join Discord")
        self.discord_button.setStyleSheet("""
            QPushButton {
                background-color: #5865F2;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4752C4;
            }
        """)
        self.discord_button.clicked.connect(self.open_discord)
        button_layout.addWidget(self.discord_button)
        
        button_layout.addStretch()
        
        # Submit button
        self.submit_button = QPushButton("Submit Feedback")
        self.submit_button.clicked.connect(self.submit_feedback)
        button_layout.addWidget(self.submit_button)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def open_discord(self):
        """Open Discord invite link in browser"""
        QDesktopServices.openUrl(QUrl("https://discord.gg/ykkkjwDnAD"))
    
    def submit_feedback(self):
        """Save feedback locally (admin dashboard integration coming later)"""
        subject = self.subject_input.text().strip()
        feedback = self.feedback_text.toPlainText().strip()
        email = self.email_input.text().strip()
        
        if not subject:
            QMessageBox.warning(self, "Missing Subject", "Please enter a subject for your feedback.")
            return
        
        if not feedback:
            QMessageBox.warning(self, "Missing Feedback", "Please enter your feedback.")
            return
        
        # Create feedback object
        feedback_data = {
            'timestamp': datetime.now().isoformat(),
            'user_id': self.user_id,
            'username': self.username,
            'email': email if email else 'not_provided',
            'subject': subject,
            'feedback': feedback,
            'version': '0.099.021'
        }
        
        # Save to local file (will be synced to admin dashboard in future)
        self.save_feedback(feedback_data)
        
        QMessageBox.information(
            self,
            "Feedback Submitted",
            "Thank you for your feedback!\\n\\n"
            "Your feedback has been saved locally.\\n"
            "Admin dashboard integration coming in future update.\\n\\n"
            "Join our Discord for updates!"
        )
        
        self.accept()
    
    def save_feedback(self, feedback_data):
        """Save feedback to local JSON file"""
        # Get app directory
        if hasattr(self.parent(), 'db'):
            app_path = self.parent().db.app_path
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))
        
        feedback_dir = os.path.join(app_path, 'data', 'feedback')
        os.makedirs(feedback_dir, exist_ok=True)
        
        feedback_file = os.path.join(feedback_dir, 'feedback_submissions.json')
        
        # Load existing feedback
        if os.path.exists(feedback_file):
            try:
                with open(feedback_file, 'r') as f:
                    all_feedback = json.load(f)
            except:
                all_feedback = []
        else:
            all_feedback = []
        
        # Append new feedback
        all_feedback.append(feedback_data)
        
        # Save back to file
        with open(feedback_file, 'w') as f:
            json.dump(all_feedback, f, indent=2)
