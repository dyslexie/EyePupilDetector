from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QInputDialog, QLabel, QSizePolicy, QSlider, QLineEdit
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
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


        self.hough_desc = QLabel("Hough radius range: ", self)
        self.hough_desc.move(15,240)

        self.min_rad = 7
        self.max_rad = 11

        self.set_min_button = QPushButton("Set MIN range (" + str(self.min_rad) + ")", self)
        self.set_min_button.clicked.connect(self.min_rad_changed)
        self.set_min_button.move(10,260)

        self.set_max_button = QPushButton("Set MAX range (" + str(self.max_rad) + ")",self)
        self.set_max_button.clicked.connect(self.max_rad_changed)
        self.set_max_button.move(10,290)


        #self.hough_slider.valueChanged[int].connect(self.change_fps_value)
        #self.hough = 25

        self.fps_slider_desc = QLabel("FPS: " + str(25), self)
        self.fps_slider_desc.move(70,330)

        self.fps_slider = QSlider(Qt.Horizontal,self)
        self.fps_slider.setMinimum(5)
        self.fps_slider.setMaximum(60)
        self.fps_slider.setValue(25)
        self.fps_slider.setTickPosition(QSlider.TicksBelow)
        self.fps_slider.setTickInterval(5)
        self.fps_slider.move(40,360)
        self.fps_slider.valueChanged[int].connect(self.change_fps_value)
        self.fps = 25

        self.photo_description1 = QLabel("Original:", self)
        self.photo_description1.move(250,10)
        self.photo_label = QLabel(self)
        self.photo_label.move(160,30)

        self.photo_description2 = QLabel("Detected:", self)
        self.photo_description2.move(520,10)
        self.photo_label2 = QLabel(self)
        self.photo_label2.move(420,30)

        self.video_preview_description = QLabel("Video Preview:", self)
        self.video_preview_description.move(360,180)
        self.video_preview = QLabel(self)
        self.video_preview.move(180,200)

        self.update_first_photo("original.jpg")
        self.update_second_photo("detected.jpg")

        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle('Eye Pupil Detector')
        self.show()

    def change_fps_value(self, value):
        self.fps_slider_desc.setText("FPS: " + str(value))
        self.fps = value

    def min_rad_changed(self, value):
        num,ok = QInputDialog.getInt(self, 'Hough', "Give MIN value of radius: ")
        self.min_rad = num
        if ok:
            self.set_min_button.setText("Set MIN range (" + str(self.min_rad) + ")")

    def max_rad_changed(self, value):
        num,ok = QInputDialog.getInt(self, 'Hough', "Give MAX value of radius: ")
        self.max_rad = num
        if ok:
            self.set_max_button.setText("Set MAX range (" + str(self.max_rad) + ")")

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
        new = perform_hough_transform("original.jpg", self.min_rad, self.max_rad)
        print("Performed Hough transform with parameters: " + str(self.min_rad) + ", " + str(self.max_rad))
        cv2.imwrite("detected.jpg", new)
        self.update_second_photo("detected.jpg")

    def getStringFromUser(self, message):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', message)
        if ok:
            return text
        return ""

