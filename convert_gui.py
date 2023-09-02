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

    def initUI(self):
        self.setGeometry(100, 100, 625, 400)
        self.setWindowTitle('File Converter')

        self.layout = QVBoxLayout()

        self.convert_ind_file.setChecked(True)
        self.convert_ind_file.clicked.connect(self.hideBatchOptions)
        
        self.title_label = QLabel('Python Image and Video Converter', self)
        
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(1)
        effect.setXOffset(5);
        effect.setYOffset(5);
        color = QColor()  
        effect.setColor(QColor.black(color))
        
        self.title_label.setGraphicsEffect(effect)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: white; background-color: #3498db; height: 20px")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.format_label = QLabel('Supported formats: Images - PNG, JPG, TIFF, WEBP, BMP, and more... | Videos - MKV, MP4', self)
        self.format_label.setStyleSheet("font-size: 17px; margin: 0;")
        self.format_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.format_label)
        

        self.image_button = QPushButton('Convert Image', self)
        self.image_button.setStyleSheet('QPushButton{ border: 1px solid gray; padding: 8px; border-radius: 4px; background-color: white; } QPushButton:hover { background-color: lightblue; }')
        self.image_button.clicked.connect(self.convertImage)

        self.layout.addWidget(self.image_button)

        self.video_button = QPushButton('Convert Video', self)
        self.video_button.setStyleSheet('QPushButton{ border: 1px solid gray; padding: 8px; border-radius: 4px; background-color: white; } QPushButton:hover { background-color: lightblue; }' )
        self.video_button.clicked.connect(self.convertVideo)
        
        self.layout.addWidget(self.video_button)

        self.ind_central_widget = QWidget()
        self.ind_central_widget.setLayout(self.layout)

        self.ind_central_widget.setStyleSheet('background-color: #d8d8d8;')
        self.setCentralWidget(self.ind_central_widget)

    def convertImage(self):
        fd = QFileDialog()
        options = fd.options()
        
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (' + self.supported_imgs_file_dialog + ')', options=options)

        if image_path:
            new_ext, _ = QFileDialog.getSaveFileName(self, 'Save Image As', '', 'Image Files (' + self.supported_imgs_file_dialog + ')')

            if new_ext:
                self.performImageConversion(image_path, new_ext)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    sys.exit(app.exec())