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
        frame_width = int(self.cam.get(3))
        frame_height = int(self.cam.get(4))
    
        # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
        out = cv2.VideoWriter(filename+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
        
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
        cv2.destroyAllWindows()
