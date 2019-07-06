afrom __future__ import print_function
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
import boto3 #Amazon web service 
import click 
import time
import datetime 
import requests # This and flask request library are NOT the same thing!
import cv2 

app = Flask(__name__)
serving_client = tf_serving_client.TFServingClient()
# rekog_client = boto3.client('rekognition')
# dlib_preprocessor = image_preprocessor_dlib.DlibPreprocessor()
mtcnn_preprocessor = image_preprocessor.MTCNNPreprocessor()
if config.USE_DLIB:
    preprocessor = dlib_preprocessor
elif config.USE_MTCNN:
    preprocessor = mtcnn_preprocessor

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
    image_str = json_data['Image']
    image_shape = ast.literal_eval(json_data['Shape'])
    image_id = json_data['ID']
    image = np.frombuffer(base64.b64decode(image_str), dtype=np.float64)
    image = image.astype(np.uint8)    
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

"""    embeddings = serving_client.send_inference_request(image_preprocessed)
route for sanitizer clients
request payload format:
{'NodeID': node_id, 'Timestamp': timestamp, 'Image': image_64str, 'Shape': image_shape}
Responses: {'Status': no face'}/{'Status': 'face'}
"""
@app.route('/sanushost/api/v1.0/sanitizer_img', methods=['POST'])
def receive_sanitizer_image():
    a = time.time()
    current_time = time.time()
    current_time1 = time.time()
    json_data = request.get_json()
    #print("request.get_json time: " + str(time.time() - current_time))
    image_str = json_data['Image']
    current_time = time.time()
    #print("json_data['Image'] time: " + str(time.time() - current_time))
    timestamp = json_data['Timestamp']
    current_time = time.time()
    node_id = json_data['NodeID']
    #print("json_data['NodeID'] time: " + str(time.time() - current_time))
    #print("Entire unload json time: " + str(time.time() - current_time1))
    current_time = time.time()
    image_shape = ast.literal_eval(json_data['Shape'])

    # image_str_b64 = base64.b64decode(image_str)
    image = np.frombuffer(base64.b64decode(image_str), dtype=np.float64)
    image = image.astype(np.uint8)
    image = np.reshape(image, image_shape)
    #print("Reshape Image: " + str(time.time() - current_time))

    if config.USE_MTCNN:
        image = image[...,::-1]

    current_time = time.time()    
    image_preprocessed = preprocessor.process(cv2.flip(image, -1))
    #print("Mtcnn process time: " + str(time.time() - current_time))

    if image_preprocessed.size == 0:
        return json.dumps({'Status': 'no face', 'Staff' : 'None'})

    current_time = time.time()    
    embeddings = serving_client.send_inference_request(image_preprocessed)
    #print("Tensorflow processor time: " + str(time.time() - current_time))

    current_time = time.time()
    graph.demo_update_node(embeddings, timestamp, node_id)
    #print("Update node time: " + str(time.time() - current_time))

    ### Druid Decoration ###
    current_time = time.time()
    staff_id = graph.demo_check_staff(embeddings)
    
    if staff_id: 
        payload = {
            'time' : datetime.datetime.utcnow().isoformat(),
            'type' : 'Dispenser',
            'nodeID' : node_id,
            'staffID' : staff_id,
            'unit' : 'ICU',
            'room_number' : '25',
            'response_type' : 'None',
            'response_message' : 'None',
        }
        try:
            response = requests.post('http://192.168.0.107:8200/v1/post/hospital', 
                json=payload, 
                headers={'Content_Type': 'application/json'}
            )
            print(response.json())
        except Exception as e:
            print(e)
            
    #print("Druid time: " + str(time.time() - current_time))
    print("Total process time for node(" + str(node_id) + "): " + str(time.time() - a))
    return json.dumps({'Status': 'face', 'Staff' : staff_id})

"""
route for entry clients
request payload format:
#TODO: add image shape information in payload
{'Timestamp': tiemstamp, 'NodeID': node_id, 'Image': [image_64str], 'Shape': image_shape}
Responses: {'Status': no face'}/{'Status': 'face'}/{'JobID': job_id}
"""
@app.route('/sanushost/api/v1.0/entry_img', methods=['POST'])
def receive_entry_image():    
    ## For debug use, remove when production
    a = time.time()

    ## TODO implement a check on payload.
    ## if any format violates the rules, stop the process. 
    json_data = request.get_json()
    timestamp = json_data['Timestamp']
    node_id = json_data['NodeID']
    image_shape = ast.literal_eval(json_data['Shape'])
    image_str = str.encode(json_data['Image'])
    image = np.frombuffer(base64.b64decode(image_str), dtype=np.float64)
    image = image.astype(np.uint8)
    image = np.reshape(image, image_shape)

    if config.USE_MTCNN:
        image = image[...,::-1]
    image_preprocessed = preprocessor.process(image)
    if image_preprocessed.size == 0:
        return json.dumps({'Staff': 0, 'Result': None})
    embeddings = serving_client.send_inference_request(image_preprocessed)
    staff_list = graph.demo_check_breach(embeddings, timestamp)

    ## For debug use, remove when production
    print("Total process time for node(" + str(node_id) + "): " + str(time.time() - a))

    return json.dumps({'Staff': 1, 'Result': staff_list})
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
