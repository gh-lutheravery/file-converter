import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QLineEdit, 
QVBoxLayout, QWidget, QFrame, QMessageBox, QGraphicsDropShadowEffect, QHBoxLayout, QRadioButton)
from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

import moviepy.editor as moviepy
from PIL import Image
import os


class ConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    sys.exit(app.exec())