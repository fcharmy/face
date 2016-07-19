import cv2
from django.conf import settings
from ..apps import FaceTechConfig


class FaceDetector(object):
    def __init__(self, casc_path=FaceTechConfig.CASCADE_CLASSIFIER_PATH):
        self.faceCascade = cv2.CascadeClassifier(casc_path)

    def find_face_path(self, image):
        """ inpurt image: numpy array"""
        if image is not None:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return self.faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))

        return None
