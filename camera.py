import cv2
from cv2 import *
import _thread
import PyQt5.QtGui
from PyQt5.QtGui import QPixmap, QImage


class Camera:
    def __init__(self):
        self.cam = VideoCapture(0)

    def take_photo(self, filename):
        s,img = self.cam.read()
        imwrite(filename,img)

    def make_video_thread(self, filename, master_thread):
         _thread.start_new_thread( self.make_video, (filename, master_thread, ) )

    def make_video(self, filename, master_thread):
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('.avi',fourcc, 30.0, (640,480))
        
        while(master_thread.video_is_recording):
            ret, frame = self.cam.read()
            if ret==True:
                out.write(frame)
                height, width, channel = frame.shape
                bytesPerLine = 3 * width
                qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
                qImg = qImg.rgbSwapped()
                master_thread.photo_label.setPixmap(QPixmap.fromImage(qImg).scaled(240,140))
                #cv2.imshow('frame',frame)
            else:
                break
        out.release()
        cv2.destroyAllWindows()
