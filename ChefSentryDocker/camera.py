import cv2
from cv2 import *
from time import sleep



class Camera:
    def __init__(self, cam_port):
        self.cam_port = cam_port
        #camera.resolution = (1024, 768)

    def take_picture(self, path, pic_name):
        self.cam = cv2.VideoCapture(-1)
        # reading the input using the camera
        result, image = self.cam.read()
        self.cam.release()
        # If image will detected without any error,
        # show result
        if result:

            # showing result, it take frame name and image
            # output
            # cv2.imshow(pic_name, image)

            # saving image in local storage
            cv2.imwrite(path, image)

            # If keyboard interrupt occurs, destroy image
            # window
            # cv2.destroyWindow(pic_name)

            # If captured image is corrupted, moving to else part
        else:
            print("No image detected. Please! try again")