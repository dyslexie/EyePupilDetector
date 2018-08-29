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
from time import sleep
from hough_transform import perform_hough_transform, perform_hough_transforms_and_return_circles
import csv


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
        self.go_to_frame_button.clicked.connect(self.go_to_frame_clicked)
        self.go_to_frame_button.move(10, 360)

        self.create_label_for_output_parameters(10,390)

        self.output_button = QPushButton("Generate output!", self)
        self.output_button.clicked.connect(self.generate_output)
        self.output_button.move(170, 440)

        self.create_control_buttons(170, 470)

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


    def create_control_buttons(self, width, height):
        self.play = QPushButton("Play", self)
        self.play.clicked.connect(self.analyze)
        self.stop = QPushButton("Stop", self)
        self.stop.clicked.connect(self.stop_video)
        self.faster = QPushButton("Faster", self)
        self.faster.clicked.connect(self.increase_speed_of_video)
        self.slower = QPushButton("Slower", self)
        self.slower.clicked.connect(self.decrease_speed_of_video)
        self.reset = QPushButton("Reset", self)
        self.reset.clicked.connect(self.reset_video)

        self.speed_label = QLabel("Speed = x 1.00  ", self)
        self.speed_label.move(width + 10, height + 40)

        self.slower.move(width, height)
        self.stop.move(width + 80, height)
        self.play.move(width + 150, height)
        self.reset.move(width + 210, height)
        self.faster.move(width + 280, height)

    def stop_video(self):
        self.is_stopped = True

    def increase_speed_of_video(self):
        self.video_speed = self.video_speed + 0.1
        self.speed_label.setText("Speed = x "+"%.2f"%self.video_speed)

    def decrease_speed_of_video(self):
        self.video_speed = self.video_speed - 0.1
        self.speed_label.setText("Speed = x "+"%.2f"%self.video_speed)
    
    def reset_video(self):
        self.go_to_frame(0)

    def generate_output(self):
        filename = self.get_string_from_user("Output filename: ")

        self.start_frame = int(self.start_frame_input.toPlainText())
        self.stop_frame = int(self.stop_frame_input.toPlainText())
        self.min_rad = int(self.min_rad_input.toPlainText())
        self.max_rad = int(self.max_rad_input.toPlainText())

        video_analyzer = VideoCapture(self.filename)
        video_analyzer.set(CAP_PROP_POS_FRAMES, self.start_frame)
        difference = int(self.stop_frame - self.start_frame)
        list_of_circles = []
        current_frame = self.stop_frame

        for x in range(difference):
            flag, frame = video_analyzer.read()
            circles = perform_hough_transforms_and_return_circles(frame, self.min_rad, self.max_rad)
            list_of_circles.append((current_frame, circles))
            current_frame = current_frame + 1
        
        self.save_list_to_file(filename, list_of_circles)
        print(list_of_circles)



    def save_list_to_file(self, filename, list_of_circles):
        with open(filename, 'w') as csvfile:
            for circle in list_of_circles:
                csvfile.write(str(circle[0]))
                csvfile.write(",")
                for x in range(3):
                    csvfile.write(str(circle[1][0][0][x]))
                    csvfile.write(",")
                csvfile.write("\n")

    def create_label_for_output_parameters(self, width, height):
        output_parameter_label = QLabel("Output parameters configuration:", self)
        start_frame_label = QLabel("Start Frame:", self)
        stop_frame_label = QLabel("Stop Frame:", self)
        min_rad_label = QLabel("Min Rad Label:", self)
        max_rad_label = QLabel("Max Rad Label:", self)
        output_parameter_label.move(width, height)
        start_frame_label.move(width, height + 30)
        stop_frame_label.move(width, height + 60)
        min_rad_label.move(width, height + 90)
        max_rad_label.move(width, height + 120)

        input_width = width + 100
        self.start_frame_input = QTextEdit("0", self)
        self.start_frame_input.resize(50,26)
        self.stop_frame_input = QTextEdit("0", self)
        self.stop_frame_input.resize(50,26)
        self.min_rad_input = QTextEdit("0", self)
        self.min_rad_input.resize(50,26)
        self.max_rad_input = QTextEdit("0", self)
        self.max_rad_input.resize(50,26)

        self.start_frame_input.move(input_width, height + 30)
        self.stop_frame_input.move(input_width, height + 60)
        self.min_rad_input.move(input_width, height + 90)
        self.max_rad_input.move(input_width, height + 120)

    def go_to_frame_clicked(self):
        frame = self.frame_number_input.toPlainText()
        self.go_to_frame(frame)

    def go_to_frame(self, frame):
        frame_number = float(frame)
        self.video.set(CAP_PROP_POS_FRAMES,frame_number)
        flag, frame = self.video.read()
        if flag:
            self.frame_number_label.setText("Frame number: " + "%.0f"%frame_number)
            self.update_preview(frame)

    def set_default_settings(self):
        self.filename = "example.avi"
        self.is_stopped = False
        self.video_speed = 1.00
        self.update_file_properties()
        self.setGeometry(100, 100, 540, 540)
        self.setWindowTitle('VideoAnalyzer')
        self.show()

    def load_filename(self):
        text = self.get_string_from_user("Get filename")
        self.filename_label.setText("Present filename: " + text)
        self.filename = text
        self.update_file_properties()

    def update_file_properties(self):
        information = ""
        self.video = VideoCapture(self.filename)
        information += "Width: " + "%.0f"%self.video.get(CAP_PROP_FRAME_WIDTH) + "\n"
        information += "Height: " + "%.0f"%self.video.get(CAP_PROP_FRAME_HEIGHT) + "\n"
        information += "Number of frames: " + "%.0f"%self.video.get(CAP_PROP_FRAME_COUNT) + "\n"
        information += "Frame per second: " + "%.0f"%self.video.get(CAP_PROP_FPS)

        self.file_information_box.clear()
        self.file_information_box.appendPlainText(information)

    def update_preview(self, frame):
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        qImg = qImg.rgbSwapped()
        self.video_preview.setPixmap(QPixmap.fromImage(qImg).scaled(480,270))

    def video_update_thread(self,filename):
        flag = True
        while(flag and not self.is_stopped):
            flag, frame = self.video.read()
            frame_number = self.video.get(CAP_PROP_POS_FRAMES)
            self.frame_number_label.setText("Frame number: " + "%.0f"%frame_number)
            if frame is not None:
                sleep(0.3/(self.video.get(CAP_PROP_FPS)*self.video_speed))
                self.update_preview(frame)
                self.show()

    def video_convert_thread(self, filename):
        flag = True
        while(flag):
            flag, frame = self.video.read()
            frame_number = self.video.get(CAP_PROP_POS_FRAMES)
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
        self.is_stopped = False
        _thread.start_new_thread( self.video_update_thread, (filename, ) )

    def get_string_from_user(self, message):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', message)
        if ok:
            return text
        return ""

app = QApplication(sys.argv)

analyzer = VideoAnalyzer()

sys.exit(app.exec_())