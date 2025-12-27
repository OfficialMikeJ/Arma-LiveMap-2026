#!/usr/bin/env python3
"""
Admin Dashboard for Arma Reforger Live Map
View and manage user feedback submissions
"""

import sys
import os
import json
from datetime import datetime

# Check if PySide6 is available
try:
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                    QHBoxLayout, QTableWidget, QTableWidgetItem,
                                    QPushButton, QLabel, QTextEdit, QMessageBox,
                                    QHeaderView, QSplitter, QGroupBox)
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QColor
except ImportError:
    print("Error: PySide6 is required to run the admin dashboard.")
    print("Install with: pip install PySide6")
    sys.exit(1)

from gui.styles import DARK_THEME


class AdminDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.feedback_file = None
        self.feedback_data = []
        self.setWindowTitle("Arma Reforger Live Map - Admin Dashboard")
        self.setMinimumSize(1200, 700)
        self.setStyleSheet(DARK_THEME)
        self.setup_ui()
        self.load_feedback()
    
    def setup_ui(self):
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Admin Dashboard - Feedback Management")
        title.setStyleSheet("font-size: 18pt; font-weight: bold; color: #5a7a51; padding: 10px;")
        layout.addWidget(title)
        
        # Statistics
        stats_group = QGroupBox("Statistics")
        stats_layout = QHBoxLayout()
        self.total_label = QLabel("Total Feedback: 0")
        self.total_label.setStyleSheet("font-size: 12pt; color: #5a7a51;")
        stats_layout.addWidget(self.total_label)
        stats_layout.addStretch()
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Splitter for table and details
        splitter = QSplitter(Qt.Vertical)
        
        # Feedback table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Date/Time", "Username", "Email", "Subject", "Version"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        splitter.addWidget(self.table)
        
        # Details panel
        details_widget = QWidget()
        details_layout = QVBoxLayout()
        details_layout.addWidget(QLabel("Feedback Details:"))
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setStyleSheet("background-color: #1a1a1a; border: 1px solid #3a3a3a;")
        details_layout.addWidget(self.details_text)
        details_widget.setLayout(details_layout)
        splitter.addWidget(details_widget)
        
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("↻ Refresh")
        refresh_btn.clicked.connect(self.load_feedback)
        button_layout.addWidget(refresh_btn)
        
        export_btn = QPushButton("📄 Export to CSV")
        export_btn.clicked.connect(self.export_to_csv)
        button_layout.addWidget(export_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        central.setLayout(layout)
    
    def load_feedback(self):
        """Load feedback from JSON file"""
        # Try to find feedback file
        possible_paths = [
            'data/feedback/feedback_submissions.json',
            '../data/feedback/feedback_submissions.json',
            'desktop_app/data/feedback/feedback_submissions.json'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self.feedback_file = path
                break
        
        if not self.feedback_file:
            QMessageBox.warning(self, "No Feedback", "No feedback submissions found.")
            return
        
        try:
            with open(self.feedback_file, 'r') as f:
                self.feedback_data = json.load(f)
            
            self.update_table()
            self.total_label.setText(f"Total Feedback: {len(self.feedback_data)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load feedback: {e}")
    
    def update_table(self):
        """Update feedback table"""
        self.table.setRowCount(len(self.feedback_data))
        
        for row, feedback in enumerate(self.feedback_data):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            
            # Date/Time
            timestamp = feedback.get('timestamp', 'N/A')
            try:
                dt = datetime.fromisoformat(timestamp)
                date_str = dt.strftime('%Y-%m-%d %H:%M')
            except:
                date_str = timestamp
            self.table.setItem(row, 1, QTableWidgetItem(date_str))
            
            # Username
            self.table.setItem(row, 2, QTableWidgetItem(feedback.get('username', 'N/A')))
            
            # Email
            email = feedback.get('email', 'not_provided')
            self.table.setItem(row, 3, QTableWidgetItem(email if email != 'not_provided' else 'N/A'))
            
            # Subject
            self.table.setItem(row, 4, QTableWidgetItem(feedback.get('subject', 'N/A')))
            
            # Version
            self.table.setItem(row, 5, QTableWidgetItem(feedback.get('version', 'N/A')))
    
    def on_selection_changed(self):
        """Handle row selection"""
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        if 0 <= row < len(self.feedback_data):
            feedback = self.feedback_data[row]
            
            details = f"""Feedback Details
{'=' * 60}

ID: {row + 1}
Date/Time: {feedback.get('timestamp', 'N/A')}
User ID: {feedback.get('user_id', 'N/A')}
Username: {feedback.get('username', 'N/A')}
Email: {feedback.get('email', 'not_provided')}
Version: {feedback.get('version', 'N/A')}

Subject:
{feedback.get('subject', 'N/A')}

Feedback:
{feedback.get('feedback', 'N/A')}
"""
            self.details_text.setPlainText(details)
    
    def export_to_csv(self):
        """Export feedback to CSV file"""
        try:
            import csv
            from datetime import datetime
            
            filename = f"feedback_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Timestamp', 'User ID', 'Username', 'Email', 'Subject', 'Feedback', 'Version'])
                
                for idx, feedback in enumerate(self.feedback_data):
                    writer.writerow([
                        idx + 1,
                        feedback.get('timestamp', ''),
                        feedback.get('user_id', ''),
                        feedback.get('username', ''),
                        feedback.get('email', ''),
                        feedback.get('subject', ''),
                        feedback.get('feedback', ''),
                        feedback.get('version', '')
                    ])
            
            QMessageBox.information(self, "Success", f"Feedback exported to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export: {e}")


def main():
    app = QApplication(sys.argv)
    dashboard = AdminDashboard()
    dashboard.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
