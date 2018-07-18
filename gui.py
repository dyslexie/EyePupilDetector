from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QInputDialog, QLabel, QSizePolicy
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QPixmap
from camera import Camera
from hough_transform import perform_hough_transform
import logging
import cv2

class UserInterface(QWidget):

    def __init__(self):
        super(UserInterface, self).__init__()
        self.video_is_recording = False
        self.camera = Camera()
        self.initUI()

    def initUI(self):

        load_img_button = QPushButton('Take photo', self)
        load_img_button.clicked.connect(self.take_photo)
        load_img_button.resize(load_img_button.sizeHint())
        load_img_button.move(10, 10)

        transform_button = QPushButton('Hough Transform', self)
        transform_button.clicked.connect(self.transform)
        transform_button.resize(transform_button.sizeHint())
        transform_button.move(10, 40)

        make_video_button = QPushButton("Start Video", self)
        make_video_button.clicked.connect(self.make_video)
        make_video_button.resize(make_video_button.sizeHint())
        make_video_button.move(10,70)

        stop_video_button = QPushButton("Stop Video", self)
        stop_video_button.clicked.connect(self.stop_video)
        stop_video_button.resize(stop_video_button.sizeHint())
        stop_video_button.move(10,100)

        self.photo_description1 = QLabel("Original:", self)
        self.photo_description1.move(250,10)
        self.photo_label = QLabel(self)
        self.photo_label.move(160,30)

        self.photo_description2 = QLabel("Detected:", self)
        self.photo_description2.move(520,10)
        self.photo_label2 = QLabel(self)
        self.photo_label2.move(420,30)

        self.video_preview_description = QLabel("Video Preview:", self)
        self.video_preview_description.move(340,180)
        self.video_preview = QLabel(self)
        self.video_preview.move(160,200)

        self.update_first_photo("original.jpg")
        self.update_second_photo("detected.jpg")

        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('Eye Pupil Detector')
        self.show()


    def update_first_photo(self, filename):
        pixmap = QPixmap(filename)
        self.photo_label.setPixmap(pixmap.scaled(240,140))
        self.video_preview.setPixmap(pixmap.scaled(480,270))

    def update_second_photo(self, filename):
        pixmap = QPixmap(filename)
        self.photo_label2.setPixmap(pixmap.scaled(240,140))

    def take_photo(self):
        self.camera.take_photo("original.jpg")
        self.update_first_photo("original.jpg")

    def make_video(self):
        filename = self.getStringFromUser("Give filename: ")
        self.video_is_recording = True
        self.camera.make_video_thread(filename, self)

    def stop_video(self):
        self.video_is_recording = False

    def transform(self):
        new = perform_hough_transform("original.jpg")
        cv2.imwrite("detected.jpg", new)
        self.update_second_photo("detected.jpg")

    def getStringFromUser(self, message):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', message)
        if ok:
            return text
        return ""

