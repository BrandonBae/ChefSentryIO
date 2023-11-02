from picamera import PiCamera
from time import sleep



class Camera:
    def __init__(self):
        self.camera = PiCamera()
        camera.resolution = (1024, 768)

    def take_picture(self, path):
        camera.start_preview()

        sleep(2)
        camera.capture('test_photo.jpg')