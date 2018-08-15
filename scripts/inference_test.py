from __future__ import print_function

import tensorflow as tf
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
import sys, dlib
import numpy as np
import scipy.misc

def predictResponse_into_nparray(response, output_tensor_name):
    dims = response.outputs[output_tensor_name].tensor_shape.dim
    shape = tuple(d.size for d in dims)
    return np.reshape(response.outputs[output_tensor_name].float_val, shape)

host = '0.0.0.0'
port = 8500
channel = implementations.insecure_channel(host, port)
stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

cnn_detector = dlib.cnn_face_detection_model_v1('/home/billyzheng/sanus_face_server/model/mmod_human_face_detector.dat')
sp = dlib.shape_predictor('/home/billyzheng/sanus_face_server/model/shape_predictor_5_face_landmarks.dat')
image = dlib.load_rgb_image('/home/billyzheng/Downloads/klaus2.jpg')
image = scipy.misc.imresize(image, 0.8)
dets = cnn_detector(image, 1)
faces = dlib.full_object_detections()
for detection in dets:
    faces.append(sp(image, detection.rect))
faces_list = np.asarray(dlib.get_face_chips(image, faces, 160))
b, h, w, c = faces_list.shape

request = predict_pb2.PredictRequest()
request.model_spec.name = 'saved_model'
request.inputs['in'].CopyFrom(tf.make_tensor_proto(faces_list, dtype=tf.float32))
request.inputs['phase'].CopyFrom(tf.make_tensor_proto(False, dtype=tf.bool))
result = stub.Predict(request, 60.0)
result_np = predictResponse_into_nparray(result, 'out')
base_emb = result_np

image2 = dlib.load_rgb_image('/home/billyzheng/Downloads/wut.jpg')
dets2 = cnn_detector(image2, 1)
faces2 = dlib.full_object_detections()
for detection2 in dets2:
	faces2.append(sp(image2, detection2.rect))
faces_list2 = np.asarray(dlib.get_face_chips(image2, faces2, 160))
request2 = predict_pb2.PredictRequest()
request2.model_spec.name = 'saved_model'
request2.inputs['in'].CopyFrom(tf.make_tensor_proto(faces_list2, dtype=tf.float32))
request2.inputs['phase'].CopyFrom(tf.make_tensor_proto(False, dtype=tf.bool))
result2 = stub.Predict(request2, 60.0)
result2_np = predictResponse_into_nparray(result2, 'out')
compare_emb = result2_np
print(np.linalg.norm(np.subtract(base_emb, compare_emb)))