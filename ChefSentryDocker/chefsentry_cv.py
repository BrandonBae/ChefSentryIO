from boil_classifier import BoilClassifier
from camera import Camera
import time

class CVModule:
    def __init__(self, pkl_path, cam_port):
        self.classifier = BoilClassifier(pkl_path)
        self.camera = Camera(cam_port)

    def predict_boil(self):
        boil_classifier_img_path = "./resources/pot_capture.png"

        self.camera.take_picture(boil_classifier_img_path, "Pot_Capture")

        prediction = self.classifier.predict("./resources/")
        return prediction[0]