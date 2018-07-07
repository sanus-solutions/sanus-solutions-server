from __future__ import print_function

import tensorflow as tf
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
import sys, dlib
import numpy as np

host = 'localhost'
port = 8500
channel = implementations.insecure_channel(host, port)
stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

cnn_detector = dlib.cnn_face_detection_model_v1('/home/billy/sanus_face_server/model/mmod_human_face_detector.dat')
sp = dlib.shape_predictor('/home/billy/sanus_face_server/model/shape_predictor_5_face_landmarks.dat')
image = dlib.load_rgb_image('/home/billy/Downloads/wjx_test_profile_blurry.jpg')
dets = cnn_detector(image, 1)
print(len(dets))
faces = dlib.full_object_detections()
for detection in dets:
    faces.append(sp(image, detection.rect))
faces_list = np.asarray(dlib.get_face_chips(image, faces, 160))
b, h, w, c = faces_list.shape
print(b, h, w, c)
request = predict_pb2.PredictRequest()
request.model_spec.name = 'saved_model'
request.inputs['in'].CopyFrom(tf.make_tensor_proto(faces_list, dtype=tf.float32, shape=[b, h, w, c]))
request.inputs['phase'].CopyFrom(tf.make_tensor_proto(False, dtype=tf.bool))
result = stub.Predict(request, 10.0)
print(result)