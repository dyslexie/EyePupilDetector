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

        pixmap = QPixmap("original.jpg")
        self.video_preview.setPixmap(pixmap.scaled(480,270))

        self.setGeometry(300, 300, 520, 310)
        self.setWindowTitle('VideoAnalyzer')
        self.show()

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

    def analyze(self,filename):
         _thread.start_new_thread( self.video_update_thread, (filename, ) )

app = QApplication(sys.argv)

analyzer = VideoAnalyzer()
analyzer.analyze("example.avi")

sys.exit(app.exec_())