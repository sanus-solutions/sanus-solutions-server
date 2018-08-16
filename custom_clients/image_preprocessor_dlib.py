"""
DLIB face alignment
HOG/CNN detector
"""
import sys, dlib
import numpy as np
from sanus_face_server.config import config

class DlibPreprocessor():
    def __init__(self):
        self.cnn_detector = dlib.cnn_face_detection_model_v1(config.DETECTOR_PATH)
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(config.PREDICTOR_PATH)

    def process(self, image):
        """
        face alignment using HOG detector
        return None if no detection, list of face chips if detection
        """
        dets = self.detector(image, 1)
        num_faces = len(dets)
        if num_faces == 0:
            return np.array([])
        faces = dlib.full_object_detections()
        for detection in dets:
            faces.append(self.sp(image, detection))
        faces_list = dlib.get_face_chips(image, faces, size=config.IMAGE_SIZE)
        return faces_list

    def cnn_process(self, image):
        """
        face alignment using CNN detector
        return None if no detection, list of face chips if detection
        """
        dets = self.cnn_detector(image, 1)
        num_faces = len(dets)
        if num_faces == 0:
            return np.array([])
        faces = dlib.full_object_detections()
        for detection in dets:
            faces.append(self.sp(image, detection.rect))
        faces_list = np.asarray(dlib.get_face_chips(image, faces, size=config.IMAGE_SIZE), dtype=np.float64)
        faces_list_w = []
        for face in faces_list:
            faces_list_w.append(self.prewhiten(face))
        faces_stack = np.stack(faces_list_w)

        return faces_stack

    def prewhiten(self, x):
        mean = np.mean(x)
        std = np.std(x)
        std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
        y = np.multiply(np.subtract(x, mean), 1/std_adj)
        return y 