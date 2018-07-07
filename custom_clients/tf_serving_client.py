from __future__ import print_function

import tensorflow as tf
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from config import config

class TFServingClient():
    def __init__(self):
        self.host = config.TF_HOST
        self.port = config.TF_PORT
        self.channel = implementations.insecure_channel(self.host, int(self.port))
        self.stub = prediction_service_pb2.beta_create_PredictionService_stub(self.channel)
        self.model_spec_name = config.MODEL_SPEC_NAME


    def send_inference_request(self, image_list):
        """
        input: image should be numpy array
        """
        b, h, w, c = image.shape
        request = predict_pb2.PredictRequest()
        request.model_spec.name = self.model_spec_name
        request.inputs['in'].CopyFrom(tf.make_tensor_proto(image, dtype=tf.float32, shape=[b, h, w, c]))
        request.inputs['phase'].CopyFrom(tf.make_tensor_proto(False, dtype=tf.bool))
        result = self.stub.Predict(request, 10.0) # 10.0s timeout
        return result
