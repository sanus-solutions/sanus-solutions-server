from __future__ import print_function

# import tensorflow as tf
from tensorflow.contrib.util import make_tensor_proto
import numpy as np
import grpc
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import os, sys
sys.path.append(os.path.abspath('..'))
from sanus_face_server.config import config
import json

class TFServingClient():
    def __init__(self):
        self.host = config.TF_HOST
        self.port = config.TF_PORT
        self.channel = grpc.insecure_channel('%s:%s' % (self.host, int(self.port)))
        self.stub = prediction_service_pb2_grpc.PredictionServiceStub(self.channel)
        self.model_spec_name = config.MODEL_SPEC_NAME

    def response_to_np(self, response, output_tensor_name):
        dims = response.outputs[output_tensor_name].tensor_shape.dim
        shape = tuple(d.size for d in dims)
        return np.reshape(response.outputs[output_tensor_name].float_val, shape)


    def send_inference_request(self, image_list):
        """
        input: image should be numpy array
        """
        request = predict_pb2.PredictRequest()
        request.model_spec.name = self.model_spec_name
        request.inputs['in'].CopyFrom(make_tensor_proto(image_list, dtype='float32'))
        request.inputs['phase'].CopyFrom(make_tensor_proto(False, dtype='bool'))
        result = self.stub.Predict(request, 10.0) # 10.0s timeout
        embeddings_np = self.response_to_np(result, 'out')
        return embeddings_np
