from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QInputDialog, QLabel, QSizePolicy, QSlider, QLineEdit, QFrame
from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from camera import Camera
from hough_transform import perform_hough_transform_on_file
from video_analyzer import VideoAnalyzer
from time import sleep
import socket
import logging
import cv2

class UserInterface(QWidget):

    def __init__(self):
        super(UserInterface, self).__init__()
        self.video_is_recording = False
        self.camera = Camera()
        self.initUI()

    def initUI(self):
        self.is_raspberry_connected = False
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

        connect_raspberry_button = QPushButton("Connect Raspberry", self)
        connect_raspberry_button.clicked.connect(self.connect_raspberry)
        connect_raspberry_button.resize(connect_raspberry_button.sizeHint())
        connect_raspberry_button.move(10,130)
        self.raspberry_label = QLabel("IP: unknown                ", self)
        self.raspberry_label.move(20,160)
        self.raspberry_label.setFrameStyle(QFrame.Panel | QFrame.Raised);

        switch_camera_button = QPushButton("Switch camera \n (PC / Raspberry)", self)
        switch_camera_button.clicked.connect(self.change_camera)
        switch_camera_button.resize(switch_camera_button.sizeHint())
        switch_camera_button.move(10,177)

        self.camera_label = QLabel("Camera : PC                ", self)
        self.camera_label.move(20, 220)
        self.camera_label.setFrameStyle(QFrame.Panel | QFrame.Raised);

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

        self.video_analyzer_button = QPushButton("Video Analyzer", self)
        self.video_analyzer_button.clicked.connect(self.video_analyzer)
        self.video_analyzer_button.move(10, 390)

        self.photo_description1 = QLabel("Original:", self)
        self.photo_description1.move(260,10)
        self.photo_label = QLabel(self)
        self.photo_label.move(170,30)

        self.photo_description2 = QLabel("Detected:", self)
        self.photo_description2.move(530,10)
        self.photo_label2 = QLabel(self)
        self.photo_label2.move(430,30)

        self.video_preview_description = QLabel("Video Preview:", self)
        self.video_preview_description.move(360,180)
        self.video_preview = QLabel(self)
        self.video_preview.move(200,200)

        self.rec_indicator = QLabel(self)
        self.rec_indicator.resize(25,45)

        self.update_first_photo("original.jpg")
        self.update_second_photo("detected.jpg")

        self.create_diode_controls(0, 420)

        self.camera.generate_preview_thread(self)
        self.setGeometry(100, 100, 700, 520)
        self.setWindowTitle('Eye Pupil Detector')
        self.show()

    def video_analyzer(self):
        self.video_analyzer = VideoAnalyzer()
        self.video_analyzer.show()

    def update_configuration(self):
        intensity = int(self.intensity_input.toPlainText())
        self.send_configuration(intensity)
        
    def send_configuration(self, intensity):
        if(self.is_raspberry_connected):
            print("Parameters: ", intensity)
            try:
                client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                client.connect((self.raspberry_ip,2222))
                client.send(("UPDATE_CONF: " + str(intensity)).encode())
                client.close()
                print("Sent update of configuration!")
            except Exception as e:
                print("Configuration not sent!")
                print("catched exception:")
                print(e)
        else:
            self.raise_no_raspberry_error()

        
    def create_diode_controls(self, width, height):
        self.send_configuration_to_raspberry = QPushButton("Update \n Raspberry Configuration", self)
        self.send_configuration_to_raspberry.clicked.connect(self.update_configuration)
        self.send_configuration_to_raspberry.move(width, height)

        self.intensity_label = QLabel("Intensity [%]: ", self)
        self.intensity_label.move(width + 10, height + 65)

        self.min_intensity_button = QPushButton("MIN", self)
        self.min_intensity_button.clicked.connect(self.send_minimum_configuration)
        self.min_intensity_button.move(width + 90, height + 65)

        self.max_intensity_button = QPushButton("MAX", self)
        self.max_intensity_button.clicked.connect(self.send_maximum_configuration)
        self.max_intensity_button.move(width + 150, height + 65)

        self.intensity_input = QTextEdit("0", self)
        self.intensity_input.resize(50,26)
        self.intensity_input.move(width + 220, height + 65)

    def send_minimum_configuration(self):
        self.send_configuration(0)

    def send_maximum_configuration(self):
        self.send_configuration(100)

    def change_camera(self):
        if(self.is_raspberry_connected):
            source = self.camera.change_camera()
            self.camera_label.setText("Camera : " + source)
            self.video_is_recording = True
            sleep(1)
            self.video_is_recording = False
            self.camera.generate_preview_thread(self)
        else:
            self.raise_no_raspberry_error()


    def connect_raspberry(self):
        ip_address = "localhost"
        ip_address = self.getStringFromUser("RaspberryPi addres: ")
        print(ip_address)
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.settimeout(5)
        try:
            client.connect((ip_address,2222))
            client.send(("UPDATE_CONF: " + str(0)).encode())
            self.raspberry_label.setText("IP: " + ip_address)
            self.raspberry_ip = ip_address
        except Exception as e:
            print(e)
            self.is_raspberry_connected = False
            self.raspberry_label.setText("IP: unknown")
            self.raise_no_raspberry_error()
            return False

        client.close()
        self.is_raspberry_connected = True
        return True

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
        rec_button_pixmap = QPixmap("rec_button_red.png")
        self.rec_indicator.setPixmap(rec_button_pixmap.scaled(25,45))
        self.rec_indicator.move(120,75)
        self.camera.make_video_thread(filename, self)

    def stop_video(self):
        self.video_is_recording = False
        self.camera.generate_preview_thread(self)
        self.rec_indicator.clear()

    def transform(self):
        new = perform_hough_transform_on_file("original.jpg", self.min_rad, self.max_rad, True)
        print("Performed Hough transform with parameters: " + str(self.min_rad) + ", " + str(self.max_rad))
        cv2.imwrite("detected.jpg", new)
        self.update_second_photo("detected.jpg")

    def raise_no_raspberry_error(self):
        self.msg = QMessageBox(self)
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setText("Raspberry not found!")
        self.msg.setWindowTitle("Error")
        self.msg.show()

    def getStringFromUser(self, message):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', message)
        if ok:
            return text
        return ""


