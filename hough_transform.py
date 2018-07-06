import cv2
import numpy as np

#create hough circles on given filename
#returns image with hough circles marked

def perform_hough_transform(filename):
    new_image = cv2.imread(filename)
    old_image = new_image.copy()

    gray_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    clahe_image = clahe.apply(gray_image)

    blur_image = cv2.medianBlur(clahe_image, 7)

    # src_gray: Input image (grayscale, blur)
    # circles: A vector that stores sets of 3 values: x_{c}, y_{c}, r for each detected circle.
    # CV_HOUGH_GRADIENT: Define the detection method. Currently this is the only one available in OpenCV
    # dp = 1: The inverse ratio of resolution
    # min_dist = src_gray.rows/8: Minimum distance between detected centers
    # param_1 = 200: Upper threshold for the internal Canny edge detector
    # param_2 = 100*: Threshold for center detection.
    # min_radius = 0: Minimum radio to be detected. If unknown, put zero as default.
    # max_radius = 0: Maximum radius to be detected. If unknown, put zero as default

    hough_circles = cv2.HoughCircles(blur_image,
                                     cv2.HOUGH_GRADIENT,
                                     1,
                                     20,
                                     param1=50,
                                     param2=30,
                                     minRadius=0,
                                     maxRadius=0)
    
    try:
        for circle in hough_circles[0,:]:
            cv2.circle(new_image,(circle[0],circle[1]),circle[2],(0,255,0),2)
            cv2.circle(old_image,(circle[0],circle[1]),2,(0,0,255),3)
    except:
        print("NO PUPIL FOUND!")

    return new_image
