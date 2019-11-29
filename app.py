from __future__ import print_function
import numpy as np
import os, sys
sys.path.append(os.path.abspath(''))
from custom_clients import tf_serving_client#, graph
# from custom_clients import image_preprocessor_dlib
from custom_clients import image_preprocessor
from custom_clients import simple_graph
from custom_clients import id_client
# from custom_clients import image_preprocessor
from flask import Flask, request
from flask.cli import AppGroup
import json, base64
import tensorflow as tf
from config import config
import ast
import click 
import time
import datetime 
import requests # This and flask request library are NOT the same thing!
import cv2

app = Flask(__name__)
serving_client = tf_serving_client.TFServingClient()
preprocessor = image_preprocessor.MTCNNPreprocessor()

id_client = id_client.IdClient()
graph = simple_graph.SimpleGraph(id_client)

"""
CLI tools
"""
@app.cli.command()
@click.argument('stat_name')
def return_stat(stat_name):
    if stat_name=='graph_size':
        click.echo('The graph has %d nodes.' % len(graph.node_list))
    else:
        click.echo('The command %s does not exist' % stat_name)


# if config.USE_MTCNN:
#     with tf.Graph().as_default():
#         gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=config.GPU_FRACTION)
#         sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
#         with sess.as_default():
#             pnet, rnet, onet = image_preprocessor.create_mtcnn(sess, None)

"""
route for adding node in graph without timestamp and embeddings
request payload format:
{'NodeID': node_id, 'Neighbors': neighbors, 'Type': node_type}
"""
@app.route('/sanushost/api/v1.0/add_node', methods=['POST'])
def add_node():
    json_data = request.get_json()
    node_id = json_data['NodeID']
    node_type = json_data['Type']
    neighbors = ast.literal_eval(json_data['Neighbors'])
    result = graph.add_node(node_id, neighbors, node_type)
    return json.dumps({'Status': result})

"""
route for adding node in graph with timestamp and embeddings
request payload format:
{'NodeID': node_id, 'Neighbors': neighbors, 'Type': node_type,
 'Embeddings': embeddings, 'Timestamp': timestamp}
"""
@app.route('/sanushost/api/v1.0/add_node_advanced', methods=['POST'])
def add_node_advanced():
    json_data = request.get_json()
    node_id = json_data['NodeID']
    node_type = json_data['Type']
    neighbors = ast.literal_eval(json_data['Neighbors'])
    embeddings = json_data['Embeddings']
    timestamp = json_data['Timestamp']
    result = graph.add_node(node_id, neighbors, node_type, embeddings, timestamp)
    return json.dumps({'Status': result})


"""
route for removing node in graph
request payload format:
{'NodeID': node_id}
"""
@app.route('/sanushost/api/v1.0/remove_node', methods=['POST'])
def remove_node():
    json_data = request.get_json()
    node_id = json_data['NodeID']
    result = graph.remove_node(node_id)
    return json.dumps({'Status': result})

"""
route for adding known faces in the collection
request payload format:
{'Image': image_64str, 'Shape': image_shape, 'ID': person_name}
Responses: {'Status': 'no face'}, {'Status': 'success'}, {'Status': 'failed'}
"""
@app.route('/sanushost/api/v1.0/add_face', methods=['POST'])
def add_face():
    json_data = request.get_json()
    image_shape = ast.literal_eval(json_data['Shape'])
    image_id = json_data['Staff']

    ## Image decoding
    image_original = base64.b64decode(json_data['Image'])
    image = np.frombuffer(image_original, dtype=np.uint8)
    image = cv2.imdecode(image, -1)
    image = np.reshape(image, image_shape)

    if config.USE_MTCNN:
        image = image[...,::-1]

    image_preprocessed = preprocessor.process(image)
    if image_preprocessed.size == 0:
        return json.dumps({'Status': 'no face'})
    embeddings = serving_client.send_inference_request(image_preprocessed)
    status = id_client.add_staff(embeddings, image_id)
    return json.dumps({'Status': status})

"""
route for removing known face in the collection by id
request payload format:
{'ID': person_name}
Response: {'Status': 'failed'} / {'Status': 'success'}
"""
@app.route('/sanushost/api/v1.0/remove_face', methods=['POST'])
def remove_face():
    json_data = request.get_json()
    remove_id = json_data['ID']
    status = id_client.remove_staff(remove_id)
    return json.dumps({'Status': status})

"""
route for detecting face and log it to druid
request payload format:
{Timestamp: time.time(), Image: base64, Shape: tuple(int)}
Response: {'Face': boolean, 'Result': string} 
"""
@app.route('/sanushost/api/v1.0/log_staff', methods=['POST'])
def log_staff():
    json_data = request.get_json()
    node_id = json_data['NodeID']
    timestamp = json_data['Timestamp']
    image_shape = ast.literal_eval(json_data['Shape'])

    ## Image decoding
    image_original = base64.b64decode(json_data['Image'])
    image = np.frombuffer(image_original, dtype=np.uint8)
    image = cv2.imdecode(image, -1)
    image = np.reshape(image, image_shape)

    if config.USE_MTCNN:
        image = image[...,::-1]
    image_preprocessed = preprocessor.process(image)

    if image_preprocessed.size == 0:
        return json.dumps({'Face': 0, 'Result': None})

    embeddings = serving_client.send_inference_request(image_preprocessed)
    staff_list = graph.log_staff(node_id,embeddings, timestamp)
    return json.dumps({'Face': 1, 'Result': staff_list})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
