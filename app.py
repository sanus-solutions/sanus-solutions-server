from __future__ import print_function
import numpy as np
import os, sys
sys.path.append(os.path.abspath(''))
from custom_clients import tf_serving_client#, graph
from custom_clients import image_preprocessor_dlib
from custom_clients import simple_graph
# from custom_clients import image_preprocessor
from flask import Flask, request
from flask.cli import AppGroup
import json, base64
import tensorflow as tf
from scipy import misc
from config import config
import ast
import boto3
import click


app = Flask(__name__)
serving_client = tf_serving_client.TFServingClient()
# rekog_client = boto3.client('rekognition')
if config.USE_DLIB:
    dlib_preprocessor = image_preprocessor_dlib.DlibPreprocessor()
graph = simple_graph.SimpleGraph()

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
route for sanitizer clients
request payload format:
{'NodeID': node_id, 'Timestamp': timestamp, 'Image': image_64str, 'Shape': image_shape}
Responses: {'Status': no face'}/{'Status': 'face'}
"""
@app.route('/sanushost/api/v1.0/sanitizer_img', methods=['POST'])
def receive_sanitizer_image():
    json_data = request.get_json()
    image_str = json_data['Image']
    timestamp = json_data['Timestamp']
    node_id = json_data['NodeID']
    image_shape = ast.literal_eval(json_data['Shape'])
    # image_str_b64 = base64.b64decode(image_str)
    image = np.frombuffer(base64.b64decode(image_str), dtype=np.float64)
    image = image.astype(np.uint8)
    image = np.reshape(image, image_shape)
    if config.USE_DLIB:
        image_preprocessed = dlib_preprocessor.cnn_process(image)
    if image_preprocessed.size == 0:
        return json.dumps({'Status': 'no face'})
    embeddings = serving_client.send_inference_request(image_preprocessed)
    print(embeddings)
    print(embeddings.shape)
    result = graph.demo_update_node(embeddings, timestamp, node_id)
    return json.dumps({'Status': 'face'})

"""
route for entry clients
request payload format:
#TODO: add image shape information in payload
{'Timestamp': tiemstamp, 'Location': location, 'Image': image_64str, 'Shape': image_shape}
Responses: {'Status': no face'}/{'Status': 'face'}/{'JobID': job_id}
"""
@app.route('/sanushost/api/v1.0/entry_img', methods=['POST'])
def receive_entry_image():
    json_data = request.get_json()
    image_str = json_data['Image']
    timestamp = json_data['Timestamp']
    location = json_data['NodeID']
    image_shape = ast.literal_eval(json_data['Shape'])
    image = np.frombuffer(base64.b64decode(image_str), dtype=np.float64)
    image = image.astype(np.uint8)
    image = np.reshape(image, image_shape)
    if config.USE_DLIB:
        image_preprocessed = dlib_preprocessor.cnn_process(image)
    if image_preprocessed.size == 0:
        return json.dumps({'Status': 'no face'})
    embeddings = serving_client.send_inference_request(image_preprocessed)
    print(embeddings)
    print(embeddings.shape)
    result = graph.demo_check_breach(embeddings, timestamp, location)
    return json.dumps({'Status': result})

"""
route to check if high-risk face is a staff or patient
payload format: 
{'Image': image_64str}
"""
@app.route('/sanushost/api/v1.0/check_staff', methods=['POST'])
def check_staff():
    # json_data = request.get_json()
    # image = json_data['Image']
    # rekog_response = rekog_client.search_faces_by_image(CollectionId='staff',
    #                                                     Image={'Bytes':image},
    #                                                     FaceMatchThreshold=70,
    #                                                     MaxFaces=2)
    #TODO: desgin response here
    return 0


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')