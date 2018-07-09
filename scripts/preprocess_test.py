import sys, dlib
import numpy as np
"""
dlib preprocessing testing script
"""

cnn_detector = dlib.cnn_face_detection_model_v1('~/sanus_face_server/model/mmod_human_face_detector.dat')
sp = dlib.shape_predictor('~/sanus_face_server/model/shape_predictor_5_face_landmarks.dat')
window = dlib.image_window()
image = dlib.load_rgb_image('~/face_tests/wjx_test_profile_blurry.jpg')
dets = cnn_detector(image, 1)
print(len(dets))
faces = dlib.full_object_detections()
for detection in dets:
    faces.append(sp(image, detection.rect))
faces_list = dlib.get_face_chips(image, faces, 160)
for image in faces_list:
    window.set_image(image)
    dlib.hit_enter_to_continue()