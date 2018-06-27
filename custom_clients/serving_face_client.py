"""
Client doing inference on image using tf serving and ResNet

Usage: serving_face_client.py [server port] [img path]

server port selected when serving the model

Author: Hongrui Zheng, Sanus Solutions
"""

from __future__ import print_function

from grpc.beta import implementations
import tensorflow as tf
import sys
from matplotlib.image import imread

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

tf.app.flags.DEFINE_string('server', 'localhost:8500', sys.argv[1])
tf.app.flags.DEFINE_string('image', '/home/billy/Downloads/wjx.jpg', sys.argv[2])
FLAGS = tf.app.flags.FLAGS


def main(_):
    host, port = FLAGS.server.split(':')
    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

    # sending request

    data = imread(FLAGS.image)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'saved_model'
    request.inputs['in'].CopyFrom(
        tf.make_tensor_proto(data, dtype='float32'))
    request.inputs['phase'].CopyFrom(
        tf.make_tensor_proto(False, dtype='bool'))
    result = stub.Predict(request, 10.0)
    print(result)

if __name__ == '__main__':
    tf.app.run()