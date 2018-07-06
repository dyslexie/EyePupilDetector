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

        self.photo_description1 = QLabel("Original", self)
        self.photo_description1.move(250,10)
        self.photo_label = QLabel(self)
        self.photo_label.move(160,30)


        self.photo_description2 = QLabel("Detected", self)
        self.photo_description2.move(520,10)
        self.photo_label2 = QLabel(self)
        self.photo_label2.move(420,30)


        self.update_first_photo("original.jpg")
        self.update_second_photo("detected.jpg")

        self.setGeometry(300, 300, 700, 200)
        self.setWindowTitle('Eye Pupil Detector')
        self.show()


    def update_first_photo(self, filename):
        pixmap = QPixmap(filename)
        self.photo_label.setPixmap(pixmap.scaled(240,140))

    def update_second_photo(self, filename):
        pixmap = QPixmap(filename)
        self.photo_label2.setPixmap(pixmap.scaled(240,140))

    def take_photo(self):
        self.camera.take_photo("original.jpg")
        self.update_first_photo("original.jpg")

    def transform(self):
        new = perform_hough_transform("original.jpg")
        cv2.imwrite("detected.jpg", new)
        self.update_second_photo("detected.jpg")



