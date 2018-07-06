from __future__ import print_function
import numpy as np
from custom_clients import tf_serving_client
from flask import Flask, jsonify, request
import sys, json

app = Flask(__name__)
serving_client = tf_serving_client.TFServingClient()
"""
"""
@app.route('/sanushost/api/v1.0/get_shit', methods=['GET'])
def image_response():
    return jsonify({'tasks': 'lolshit'})

"""
route for sanitizer clients
"""
@app.route('/sanushost/api/v1.0/sanitizer_img', methods=['POST'])
def receive_sanitizer_image():
    json_data = request.get_json()
    print(json_data)
    # TODO: receive image in JSON base 64 format, convert to numpy array
    result = serving_client.send_inference_request(json_data)
    # TODO: add embedding to graph with timestamp and location
    return json.dumps(result)

"""
route for entry clients
"""
@app.route('/sanushost/api/v1.0/entry_img', methods=['POST'])
def receive_entry_image():
    json_data = request.get_json()
    result = serving_client.send_inference_request(json_data)
    # result is face embedding vector
    # TODO: do graph search and compare here, determine if breach happend
    return json.dumps('shit')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')