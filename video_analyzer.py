import numpy as np
import cv2
from cv2 import *
from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QInputDialog, QLabel, QSizePolicy, QSlider, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import sys
import _thread
from hough_transform import perform_hough_transform



class VideoAnalyzer(QWidget):

    def __init__(self):
        super(VideoAnalyzer, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.video_preview_description = QLabel("Video Preview:", self)
        self.video_preview_description.move(10,10)
        
        self.frame_number_label = QLabel("Frame number: 0      ", self)
        self.frame_number_label.move(370, 10)

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

        self.load_filename_button = QPushButton("Convert", self)
        self.load_filename_button.clicked.connect(self.convert)
        self.load_filename_button.move(170, 330)

        self.go_to_frame_button = QPushButton("Go to frame:", self)
        self.go_to_frame_button.clicked.connect(self.go_to_frame)
        self.go_to_frame_button.move(10, 360)

        self.frame_number_input = QTextEdit("0", self)
        self.frame_number_input.resize(50,26)
        self.frame_number_input.move(125, 360)

        pixmap = QPixmap("original.jpg")
        self.video_preview.setPixmap(pixmap.scaled(480,270))

        self.file_information_box_label = QLabel("File information: ", self)
        self.file_information_box_label.move(350,310)
        self.file_information_box = QPlainTextEdit(self)
        self.file_information_box.setReadOnly(True)
        self.file_information_box.move(300,330)
        self.file_information_box.resize(200,75)

        self.set_default_settings()

    def go_to_frame(self):
        frame = self.frame_number_input.toPlainText()
        cap = VideoCapture(self.filename)
        frame_number = float(frame)
        cap.set(CAP_PROP_POS_FRAMES,frame_number)
        flag, frame = cap.read()
        if flag:
            self.frame_number_label.setText("Frame number: " + "%.0f"%frame_number)
            self.update_preview(frame)

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
            self.frame_number_label.setText("Frame number: " + "%.0f"%frame_number)
            if frame is not None:
                self.update_preview(frame)
                self.show()

    def video_convert_thread(self, filename):
        cap = VideoCapture(filename)
        flag = True
        while(flag):
            flag, frame = cap.read()
            frame_number = cap.get(CAP_PROP_POS_FRAMES)
            print(frame_number)
            if frame is not None:
                self.update_preview(frame)
                perform_hough_transform(frame, 1, 2)
                self.show()

    def convert(self):
        filename = self.filename
        _thread.start_new_thread(self.video_convert_thread, (filename, ))

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