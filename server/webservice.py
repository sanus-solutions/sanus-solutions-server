from __future__ import print_function

from grpc.beta import implementations
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

import sys, json

from flask import Flask, jsonify, request

class serving_client():
    def __init__(self, host, port, spec_name):
        self.host = host
        self.port = port
        self.channel = implementations.insecure_channel(self.host, int(self.port))
        self.stub = prediction_service_pb2.beta_create_PredictionService_stub(self.channel)
        self.model_spec_name = spec_name


    def send_inference_request(self, image):
        h, w, c = image.shape
        request = predict_pb2.PredictRequest()
        request.model_spec.name = self.model_spec_name
        # TODO: following line is for batch of 1
        request.inputs['in'].CopyFrom(tf.make_tensor_proto(image, dtype=tf.float32, shape=[1, h, w, c]))
        request.inputs['phase'].CopyFrom(tf.make_tensor_proto(False, dtype=tf.bool))
        result = self.stub.Predict(request, 10.0)
        return result


# TODO: change path here
with open('../config/config.json') as f:
    config = json.load(f)
secret_key = config['DEFAULT']['SECRET_KEY']
public_key = config['DEFAULT']['PUBLIC_KEY']
aws_region = config['DEFAULT']['AWS_REGION']
server_host = config['DEFAULT']['SERVER_HOST']
server_port = config['DEFAULT']['SERVER_PORT']
tf_host = config['DEFAULT']['TF_HOST']
tf_port = config['DEFAULT']['TF_PORT']
model_name = config['DEFAULT']['MODEL_SPEC_NAME']

# # define tf app flags
# tf.app.flags.DEFINE_string('server', 'localhost:8500', sys.argv[1])
# FLAGS = tf.app.flags.FLAGS


app = Flask(__name__)

@app.route('/sanushost/api/v1.0/get_img', methods=['GET'])
def image_response():
    return jsonify({'tasks': 'lolshit'})

@app.route('/sanushost/api/v1.0/send_img', methods=['POST'])
def receive_image():
    serving_client = serving_client(tf_host, tf_port, model_name)

    return jsonify({'response': 'lolshit'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')