"""
MTCNN face alignment
CNN detector
"""

from tensorflow.contrib.util import make_tensor_proto
import numpy as np
import grpc
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
from sanus_face_server.config import config
import cv2

class MTCNNPreprocessor():
    def __init__(self):
        self.host = config.MTCNN_HOST
        self.port = config.MTCNN_PORT
        self.channel = grpc.insecure_channel('%s:%s' % (self.host, int(self.port)))
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(self.channel)
        self.model_spec_name = config.MTCNN_MODEL_SPEC_NAME
        self.min_size = 20
        self.factor = 0.709
        self.thresholds = [0.6, 0.7, 0.7]

    def prewhiten(self, x):
        mean = np.mean(x)
        std = np.std(x)
        std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
        y = np.multiply(np.subtract(x, mean), 1/std_adj)
        return y 

    def response_to_np(self, response, output_tensor_name):
        dims = response.outputs[output_tensor_name].tensor_shape.dim
        shape = tuple(d.size for d in dims)
        return np.reshape(response.outputs[output_tensor_name].float_val, shape)

    def extract_faces(self, image, bbox, scores, face_size):
        faces_list = []
        r, c, _ = image.shape
        for idx, box in enumerate(bbox):
            if scores[idx] < 0.9:
                continue
            face = image[int(box[0]):int(box[2]), int(box[1]):int(box[3]), :]
            #face = scipy.misc.imresize(face, (face_size, face_size), 'bilinear')
            face = cv2.resize(face, (face_size, face_size))
            faces_list.append(self.prewhiten(face))
        return np.asarray(faces_list)

    def process(self, image):
        request = predict_pb2.PredictRequest()
        request.model_spec.name = self.model_spec_name
        request.inputs['in'].CopyFrom(make_tensor_proto(image, dtype='float32'))
        request.inputs['min_size'].CopyFrom(make_tensor_proto(self.min_size, dtype='float32'))
        request.inputs['factor'].CopyFrom(make_tensor_proto(self.factor, dtype='float32'))
        request.inputs['thresholds'].CopyFrom(make_tensor_proto(self.thresholds))
        result = self.stub.Predict(request, 10.0)
        bbox_np = self.response_to_np(result, 'box')
        score_np = self.response_to_np(result, 'prob')
        faces_list = self.extract_faces(image, bbox_np.clip(min=0), score_np, config.IMAGE_SIZE)
        return faces_list
