from cv2 import VideoCapture, imwrite

class Camera:
    def __init__(self):
        self.cam = VideoCapture(0)

    def take_photo(self, filename):
        s,img = self.cam.read()
        imwrite(filename,img)
