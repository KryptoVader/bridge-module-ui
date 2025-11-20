from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QSplitter, QLabel, QSizePolicy
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
import sys
import os

from ui.basic_inputs import BasicInputs


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bridge Module - UI Screening Task")
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))  # Set window icon
        self.setMinimumSize(1100, 700)

        # === Central Widget ===
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # === Left Panel (Inputs) ===
        self.basic_inputs_widget = BasicInputs()
        splitter.addWidget(self.basic_inputs_widget)
        self.basic_inputs_widget.setMinimumWidth(420)

        # === Right Panel (Reference Image) ===
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        pixmap = QPixmap(resource_path("assets/bridge_cross_section.png"))
        image_label.setPixmap(pixmap.scaled(
            500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        splitter.addWidget(image_label)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
