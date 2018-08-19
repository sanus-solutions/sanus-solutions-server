from __future__ import print_function
import os, sys
sys.path.append(os.path.abspath('..'))
from sanus_face_server.custom_clients import image_preprocessor
from sanus_face_server.custom_clients import image_preprocessor_dlib
import cv2, dlib
import scipy.misc

processor = image_preprocessor.MTCNNPreprocessor()
dlib_processor = image_preprocessor_dlib.DlibPreprocessor()

# img = cv2.imread('/home/billyzheng/Downloads/cgroup.jpg')
img = dlib.load_rgb_image('/home/billyzheng/Downloads/cgroup.jpg')
img_bgr = img[...,::-1]

faces_list = processor.process(img_bgr)
print(faces_list.shape)
faces_list_dlib = dlib_processor.process(img)
print(faces_list_dlib.shape)