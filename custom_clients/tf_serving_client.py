from __future__ import print_function

import tensorflow as tf
import numpy as np
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from config import config
import json

class TFServingClient():
    def __init__(self):
        self.host = config.TF_HOST
        self.port = config.TF_PORT
        self.channel = implementations.insecure_channel(self.host, int(self.port))
        self.stub = prediction_service_pb2.beta_create_PredictionService_stub(self.channel)
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
        request.inputs['in'].CopyFrom(tf.make_tensor_proto(image_list, dtype=tf.float32))
        request.inputs['phase'].CopyFrom(tf.make_tensor_proto(False, dtype=tf.bool))
        result = self.stub.Predict(request, 10.0) # 10.0s timeout
        embeddings_np = self.response_to_np(result, 'out')
        return {'embeddings': embeddings_np}, 200
