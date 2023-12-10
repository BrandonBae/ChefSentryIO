import fastai
from fastai.learner import load_learner
from fastai.vision.all import *
from fastai.vision import *
from fastai.vision.core import PILImage


class BoilClassifier:
    def __init__(self, pkl_path):
        self.model = load_learner(pkl_path)


    def predict(self, img_path):
        img = get_image_files(img_path)[0]
        #img = PILImage.create(img_path)
        return self.model.predict(img)
