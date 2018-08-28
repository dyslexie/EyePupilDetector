import numpy as np
import cv2
from cv2 import *
from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QInputDialog, QLabel, QSizePolicy, QSlider, QLineEdit
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import sys
import _thread



class VideoAnalyzer(QWidget):

    def __init__(self):
        super(VideoAnalyzer, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.video_preview_description = QLabel("Video Preview:", self)
        self.video_preview_description.move(10,10)
        self.video_preview = QLabel(self)
        self.video_preview.move(30,30)

        self.filename_label = QLabel("Present filename: example.avi          ", self)
        self.filename_label.move(10,310)

        self.load_filename_button = QPushButton("Load File", self)
        self.load_filename_button.clicked.connect(self.load_filename)
        self.load_filename_button.move(10, 330)



        self.load_filename_button = QPushButton("Play", self)
        self.load_filename_button.clicked.connect(self.analyze)
        self.load_filename_button.move(100, 330)

        pixmap = QPixmap("original.jpg")
        self.video_preview.setPixmap(pixmap.scaled(480,270))

        self.file_information_box_label = QLabel("File information: ", self)
        self.file_information_box_label.move(350,310)
        self.file_information_box = QPlainTextEdit(self)
        self.file_information_box.setReadOnly(True)
        self.file_information_box.move(300,330)
        self.file_information_box.resize(200,75)

        self.set_default_settings()


    def set_default_settings(self):
        self.filename = "example.avi"
        self.update_file_properties()
        self.setGeometry(100, 100, 520, 410)
        self.setWindowTitle('VideoAnalyzer')
        self.show()

    def load_filename(self):
        text = self.get_string_from_user("Get filename")
        self.filename_label.setText("Present filename: " + text)
        self.filename = text
        self.update_file_properties()

    def update_file_properties(self):
        information = ""
        video = VideoCapture(self.filename)
        information += "Width: " + "%.0f"%video.get(CAP_PROP_FRAME_WIDTH) + "\n"
        information += "Height: " + "%.0f"%video.get(CAP_PROP_FRAME_HEIGHT) + "\n"
        information += "Number of frames: " + "%.0f"%video.get(CAP_PROP_FRAME_COUNT) + "\n"
        information += "Frame per second: " + "%.0f"%video.get(CAP_PROP_FPS)



        self.file_information_box.clear()
        self.file_information_box.appendPlainText(information)

    def update_preview(self, frame):
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        qImg = qImg.rgbSwapped()
        self.video_preview.setPixmap(QPixmap.fromImage(qImg).scaled(480,270))

    def video_update_thread(self,filename):
        cap = VideoCapture(filename)
        flag = True
        while(flag):
            flag, frame = cap.read()
            frame_number = cap.get(CAP_PROP_POS_FRAMES)
            print(frame_number)
            if frame is not None:
                self.update_preview(frame)
                self.show()

    def analyze(self):
        filename = self.filename
        _thread.start_new_thread( self.video_update_thread, (filename, ) )

    def get_string_from_user(self, message):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', message)
        if ok:
            return text
        return ""

app = QApplication(sys.argv)

analyzer = VideoAnalyzer()

sys.exit(app.exec_())