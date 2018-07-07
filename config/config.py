# AWS SETTINGS
SECRET_KEY = '...'
PUBLIC_KEY = '...'
ASW_REGION = '...'

# SERVER SETTINGS
SERVER_HOST = 'localhost'
SERVER_PORT = '5000'

# TF SERVING SETTINGS
TF_HOST = 'localhost'
TF_PORT = '8500'
MODEL_SPEC_NAME = 'saved_model'

# PREPROCESSOR SETTINGS
USE_DLIB = True
USE_MTCNN = False
IMAGE_SIZE = 160
MIN_SIZE = 20
MARGIN = 44
GPU_FRACTION = 1.0
MTCNN_THRESHOLD = [0.6, 0.7, 0.7]
MTCNN_FACTOR = 0.709
DETECTOR_PATH = '/home/billy/sanus_face_server/model/mmod_human_face_detector.dat'
PREDICTOR_PATH = '/home/billy/sanus_face_server/model/shape_predictor_5_face_landmarks.dat'