import cv2
from cv2 import *
import _thread
import PyQt5.QtGui
from PyQt5.QtGui import QPixmap, QImage
from time import sleep

class Camera:
    def __init__(self):
        self.cam = VideoCapture(0)
        self.is_raspberry_connected = False

    def take_photo(self, filename):
        sleep(1)
        s,img = self.cam.read()
        imwrite(filename,img)

    def change_camera(self, raspberry_ip):
        if self.is_raspberry_connected:
            self.cam = VideoCapture(0)
            self.is_raspberry_connected = False
            return "PC"
        self.cam = VideoCapture("http://"+raspberry_ip+":8160")
        self.is_raspberry_connected = True
        return "Raspberry Pi"

    def make_video_thread(self, filename, master_thread):
         _thread.start_new_thread( self.make_video, (filename, master_thread, ) )

    def generate_preview_thread(self, master_thread):
        _thread.start_new_thread(self.make_preview, (master_thread, ))

    def make_preview(self, master_thread):
        # Define the codec and create VideoWriter object
        frame_width = int(self.cam.get(3))
        frame_height = int(self.cam.get(4))
    
        while(not master_thread.video_is_recording):
            ret, frame = self.cam.read()
            if ret==True:
                height, width, channel = frame.shape
                bytesPerLine = 3 * width
                qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
                qImg = qImg.rgbSwapped()
                master_thread.video_preview.setPixmap(QPixmap.fromImage(qImg).scaled(480,270))
            else:
                break

    def make_video(self, filename, master_thread):
        # Define the codec and create VideoWriter object
        frame_width = int(self.cam.get(3))
        frame_height = int(self.cam.get(4))
    
        # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
        out = cv2.VideoWriter(filename+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), master_thread.fps, (frame_width,frame_height))
        
        while(master_thread.video_is_recording):
            ret, frame = self.cam.read()
            if ret==True:
                out.write(frame)
                height, width, channel = frame.shape
                bytesPerLine = 3 * width
                qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
                qImg = qImg.rgbSwapped()
                master_thread.video_preview.setPixmap(QPixmap.fromImage(qImg).scaled(480,270))
            else:
                break
        out.release()
