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

        self.supported_vids = ['MKV', 'MP4']
        
        exts = Image.registered_extensions()
        supported_extensions = {ex for ex, f in exts.items() if f in Image.SAVE}
        
        self.supported_imgs = supported_extensions

        # make the supported image formats for the file dialog
        modified_strings = ["*" + s for s in self.supported_imgs]
        result_string = " ".join(modified_strings)
        
        self.supported_imgs_file_dialog = result_string
        self.initUI()

    # create main interface of the app
    def initUI(self):
        self.setGeometry(100, 100, 625, 400)
        self.setWindowTitle('File Converter')

        self.layout = QVBoxLayout()
        rb_layout = QVBoxLayout()

        self.convert_ind_file = QRadioButton('Convert Individual Files', self)
        self.convert_batch_file = QRadioButton('Convert File Batches', self)
        
        self.convert_ind_file.setChecked(True)
        self.convert_batch_file.clicked.connect(self.initBatchUI)
        self.convert_ind_file.clicked.connect(self.hideBatchOptions)

        rb_layout.addWidget(self.convert_ind_file)
        rb_layout.addWidget(self.convert_batch_file)
        
        self.title_label = QLabel('Python Image and Video Converter', self)
        
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(1)
        effect.setXOffset(5)
        effect.setYOffset(5)
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
        self.image_button.clicked.connect(self.getImagePaths)

        self.layout.addWidget(self.image_button)

        self.video_button = QPushButton('Convert Video', self)
        self.video_button.setStyleSheet('QPushButton{ border: 1px solid gray; padding: 8px; border-radius: 4px; background-color: white; } QPushButton:hover { background-color: lightblue; }' )
        self.video_button.clicked.connect(self.getVideoPaths)
        
        self.layout.addWidget(self.video_button)

        self.layout.addLayout(rb_layout)

        self.ind_central_widget = QWidget()
        self.ind_central_widget.setLayout(self.layout)

        self.ind_central_widget.setStyleSheet('background-color: #d8d8d8;')
        self.setCentralWidget(self.ind_central_widget)

    # make interface for batch conversions
    def initBatchUI(self):
        self.batch_layout = QVBoxLayout()

        self.open_button = QPushButton('Open Files', self)
        self.open_button.clicked.connect(self.openBatch)
        self.batch_layout.addWidget(self.open_button)
        
        self.output_path_button = QPushButton('Output Path', self)
        self.output_path_button.clicked.connect(self.openBatchOutput)
        self.batch_layout.addWidget(self.output_path_button)

        self.new_extension_label = QLabel('New File Extension, ex. png', self)
        self.batch_layout.addWidget(self.new_extension_label)
        self.output_path_note = QLabel('Note that any videos will be converted to either mkv or mp4.', self)
        self.batch_layout.addWidget(self.output_path_note)
        
        self.new_extension_input = QLineEdit(self)
        self.batch_layout.addWidget(self.new_extension_input)

        self.convert_button = QPushButton('Convert', self)
        self.convert_button.clicked.connect(self.convertBatch)
        self.batch_layout.addWidget(self.convert_button)
        self.layout.addLayout(self.batch_layout)


    # save file batch that user wants to convert
    def openBatch(self):
        fd = QFileDialog()
        options = fd.options()
        
        files, _ = QFileDialog.getOpenFileNames(self, 'Open Files', '', 'Image Files (' + self.supported_imgs_file_dialog + ')', options=options)
        self.selected_files = files

    
    # save directory that user wants to save converted batch to
    def openBatchOutput(self):
        fd = QFileDialog()
        options = fd.options()
        
        output_folder = QFileDialog.getExistingDirectory(self, 'Open Files', '', options=options)
        self.output_folder = output_folder

    
    # hide batch ui when switching to individual conversion
    def hideBatchOptions(self):
        # Remove batch options layout
        if self.batch_layout.count() > 0:
            num = 0
            while self.batch_layout.itemAt(num):
                self.batch_layout.itemAt(num).widget().deleteLater()
                self.layout.removeItem(self.batch_layout)
                num += 1


    def validate_ext(self, new_extension_input): 
        valid_ext = '.' + new_extension_input.lower()
        if valid_ext not in self.supported_imgs and self.supported_vids:
            err_msg = "The extension you entered isn't supported; try again."
            QMessageBox.warning(self, 'Error', err_msg)
            
            return False
            
        return True

    # loop through files in batch to convert
    def convertBatch(self):
        output_path = self.output_folder
        new_extension = self.new_extension_input.text()
        
        valid_ext_flag = self.validate_ext(self.new_extension_input.text())
        if valid_ext_flag == False:
            return

        for file_path in self.selected_files:
            file_name = file_path.split('/')[-1]  # Get the file name from the path
            old_file_ext = file_name.split('.')[1]
            new_file_name = file_name.split('.')[0] + '.' + new_extension
            new_file_path = os.path.join(output_path, new_file_name)
            
            mp4_flag = False
            vid_flag = False
            
            if old_file_ext.upper() in self.supported_vids:
                vid_flag = True
                if old_file_ext.upper() == 'MP4':
                    mp4_flag = True
                    new_file_name = file_name.split('.')[0] + '.' + 'mp4'
                new_file_name = file_name.split('.')[0] + '.' + 'mkv'
            
            if vid_flag == False:
                self.performImageConversion(file_path, new_file_path, fin_msg_flag=False)
                
            elif vid_flag == True:
                if mp4_flag:
                    self.performVideoConversion(file_path, 'mp4', fin_msg_flag=False)
                else:
                    self.performVideoConversion(file_path, 'mkv', fin_msg_flag=False)

        QMessageBox.about(self, 'Batch Conversion Finished', 'Batch conversion is complete.')


    def getVideoPaths(self):
        fd = QFileDialog()
        options = fd.options()

        video_path, _ = QFileDialog.getOpenFileName(self, 'Open Video', '', 'Video Files (*.mkv *.mp4)', options=options)

        if video_path:
            new_path, _ = QFileDialog.getSaveFileName(self, 'Save Video As', '', 'Video Files (*.mkv *.mp4)')

            if new_path:
                self.performVideoConversion(video_path, new_path)


    def getImagePaths(self):
        fd = QFileDialog()
        options = fd.options()
        
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (' + self.supported_imgs_file_dialog + ')', options=options)

        if image_path:
            new_ext, _ = QFileDialog.getSaveFileName(self, 'Save Image As', '', 'Image Files (' + self.supported_imgs_file_dialog + ')')

            if new_ext:
                self.performImageConversion(image_path, new_ext)

    def performVideoConversion(self, video_path, new_path, fin_msg_flag = True):
        try:
            clip = moviepy.VideoFileClip(video_path)
            clip.write_videofile(new_path, codec="libx264")
            
            if fin_msg_flag:
                QMessageBox.about(self, 'Conversion Finished', 'Video conversion is complete.')
            
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Error occurred during conversion: ' + str(e))


    def performImageConversion(self, image_path, new_path, fin_msg_flag = True):
        try:
            img = Image.open(image_path)

            rgb_img = img.convert('RGB')
            rgb_img.save(new_path)
            
            if fin_msg_flag:
                QMessageBox.about(self, 'Conversion Finished', 'Image conversion is complete.')
                
        except FileNotFoundError as e:
            QMessageBox.warning(self, 'Error', 'Error occurred; the sent file might not exist: ' + str(e))
        except Exception as e:
            QMessageBox.warning(self, 'Error', 'Error occurred during conversion: ' + str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    converter = ConverterApp()
    converter.show()
    sys.exit(app.exec())