# Arma Reforger Dark Theme Styles

DARK_THEME = """
QWidget {
    background-color: #1a1a1a;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
}

QMainWindow {
    background-color: #0d0d0d;
}

QLabel {
    color: #e0e0e0;
    background-color: transparent;
}

QLineEdit {
    background-color: #2a2a2a;
    border: 2px solid #3a3a3a;
    border-radius: 4px;
    padding: 8px;
    color: #e0e0e0;
    selection-background-color: #4a6741;
}

QLineEdit:focus {
    border: 2px solid #5a7a51;
}

QPushButton {
    background-color: #3a4a36;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    color: #e0e0e0;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #4a5a46;
}

QPushButton:pressed {
    background-color: #2a3a26;
}

QPushButton:disabled {
    background-color: #2a2a2a;
    color: #666666;
}

QCheckBox {
    color: #e0e0e0;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #3a3a3a;
    border-radius: 3px;
    background-color: #2a2a2a;
}

QCheckBox::indicator:checked {
    background-color: #5a7a51;
    border-color: #5a7a51;
}

QComboBox {
    background-color: #2a2a2a;
    border: 2px solid #3a3a3a;
    border-radius: 4px;
    padding: 6px;
    color: #e0e0e0;
}

QComboBox:hover {
    border: 2px solid #5a7a51;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox QAbstractItemView {
    background-color: #2a2a2a;
    border: 2px solid #3a3a3a;
    selection-background-color: #5a7a51;
    color: #e0e0e0;
}

QTabWidget::pane {
    border: 2px solid #3a3a3a;
    background-color: #1a1a1a;
}

QTabBar::tab {
    background-color: #2a2a2a;
    color: #e0e0e0;
    padding: 10px 20px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #3a4a36;
}

QTabBar::tab:hover {
    background-color: #3a3a3a;
}

QGroupBox {
    border: 2px solid #3a3a3a;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    color: #e0e0e0;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    color: #5a7a51;
}

QScrollBar:vertical {
    background-color: #1a1a1a;
    width: 12px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #3a3a3a;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background-color: #4a4a4a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QTextEdit {
    background-color: #2a2a2a;
    border: 2px solid #3a3a3a;
    border-radius: 4px;
    color: #e0e0e0;
}

QMessageBox {
    background-color: #1a1a1a;
}

QMessageBox QLabel {
    color: #e0e0e0;
}

QMessageBox QPushButton {
    min-width: 80px;
}
"""