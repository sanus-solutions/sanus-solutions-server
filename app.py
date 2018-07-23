from __future__ import print_function
import numpy as np
from custom_clients import tf_serving_client, graph
from custom_clients import image_preprocessor_dlib
from custom_clients import simple_graph
# from custom_clients import image_preprocessor
from flask import Flask, request
import sys, json, base64
import tensorflow as tf
from scipy import misc
from config import config
import ast
import boto3


app = Flask(__name__)
serving_client = tf_serving_client.TFServingClient()
rekog_client = boto3.client('rekognition')
if config.USE_DLIB:
    dlib_preprocessor = image_preprocessor_dlib.DlibPreprocessor()
graph = simple_graph.SimpleGraph()


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
{'NodeID': node_id, 'Timestamp': tiemstamp, 'Image': image_64str, 'Shape': image_shape}
"""
@app.route('/sanushost/api/v1.0/sanitizer_img', methods=['POST'])
def receive_sanitizer_image():
    json_data = request.get_json()
    image_str = json_data['Image']
    timestamp = json_data['Timestamp']
    node_id = json_data['NodeID']
    image_shape = ast.literal_eval(json_data['Shape'])
    image = np.frombuffer(base64.decodestring(image_str), dtype=np.float64)
    image = image.astype(np.uint8)
    image = np.reshape(image, image_shape)
    if config.USE_DLIB:
        image_preprocessed = dlib_preprocessor.cnn_process(image)
    # elif config.USE_MTCNN:
    #     img_list = []
    #     img_size = np.asarray(image.shape)[0:2]
    #     margin = config.MARGIN
    #     image_size = config.IMAGE_SIZE
    #     bbox, _ = image_preprocessor.detect_face(image, config.MIN_SIZE, pnet, rnet, onet, config.MTCNN_THRESHOLD, config.MTCNN_FACTOR)
    #     if len(bbox) < 1:
    #         return json.dumps({'Status': 'No Face'})
    #     det = np.squeeze(bbox[0, 0:4])
    #     bb = np.zeros(4, dtype=np.int32)
    #     bb[0] = np.maximum(det[0]-margin/2, 0)
    #     bb[1] = np.maximum(det[1]-margin/2, 0)
    #     bb[2] = np.minimum(det[2]+margin/2, img_size[1])
    #     bb[3] = np.minimum(det[3]+margin/2, img_size[0])
    #     cropped = image[bb[1]:bb[3],bb[0]:bb[2],:]
    #     aligned = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
    #     prewhitened = image_preprocessor.prewhiten(aligned)
    #     img_list.append(prewhitened)
    #     image_preprocessed = np.stack(img_list)
    # if image_preprocessed == None:
    #     return json.dumps({'Status': 'No Face'})
    embeddings = serving_client.send_inference_request(image_preprocessed)
    # print(embeddings)
    result = graph.update_node(embeddings, timestamp, node_id)
    return json.dumps({'Status': result})

"""
route for entry clients
request payload format:
#TODO: add image shape information in payload
{'Timestamp': tiemstamp, 'Location': location, 'Image': image_64str, 'Shape': image_shape}
"""
@app.route('/sanushost/api/v1.0/entry_img', methods=['POST'])
def receive_entry_image():
    json_data = request.get_json()
    image_str = json_data['Image']
    timestamp = json_data['Timestamp']
    location = json_data['Location']
    image_shape = ast.literal_eval(json_data['Shape'])
    image = np.frombuffer(base64.decodestring(image_str), dtype=np.float64)
    image = image.astype(np.uint8)
    image = np.reshape(image, image_shape)
    if config.USE_DLIB:
        image_preprocessed = dlib_preprocessor.cnn_process(image)
    # elif config.USE_MTCNN:
    #     img_list = []
    #     img_size = np.asarray(image.shape)[0:2]
    #     margin = config.MARGIN
    #     image_size = config.IMAGE_SIZE
    #     bbox, _ = image_preprocessor.detect_face(image, config.MIN_SIZE, pnet, rnet, onet, config.MTCNN_THRESHOLD, config.MTCNN_FACTOR)
    #     if len(bbox) < 1:
    #         return json.dumps({'Status': 'No Face'})
    #     det = np.squeeze(bbox[0, 0:4])
    #     bb = np.zeros(4, dtype=np.int32)
    #     bb[0] = np.maximum(det[0]-margin/2, 0)
    #     bb[1] = np.maximum(det[1]-margin/2, 0)
    #     bb[2] = np.minimum(det[2]+margin/2, img_size[1])
    #     bb[3] = np.minimum(det[3]+margin/2, img_size[0])
    #     cropped = image[bb[1]:bb[3],bb[0]:bb[2],:]
    #     aligned = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
    #     prewhitened = image_preprocessor.prewhiten(aligned)
    #     img_list.append(prewhitened)
    #     image_preprocessed = np.stack(img_list)
    # if image_preprocessed == None:
    #     return json.dumps({'Status': 'No Face'})
    embeddings = serving_client.send_inference_request(image_preprocessed)
    result = graph.check_breach(embeddings, timestamp, location)
    return json.dumps({'Status': result})

"""
route to check if high-risk face is a staff or patient
payload format: 
{'Image': image_64str}
"""
@app.route('sanushost/api/v1.0/check_staff', methods=['POST'])
def check_staff():
    json_data = request.get_json()
    image = json_data['Image']
    rekog_response = rekog_client.search_faces_by_image(CollectionId='staff',
                                                        Image={'Bytes':image},
                                                        FaceMatchThreshold=70,
                                                        MaxFaces=2)
    #TODO: desgin response here
    return 0

@app.route('/sanushost/api/v1.0/check_total_node', methods=['GET'])
def return_total_node():
    return len(graph.node_list)

@app.route('/sanushost/api/v1.0/check_alive_node', methods=['GET'])
def return_alive_node():
    return 0

@app.route('/sanushost/api/v1.0/check_tf_avg_time', methods=['GET'])
def return_serving_time():
    return 0
"""
payload format: {'NodeID': node_id}
"""
@app.route('sanushost/api/v1.0/check_node_alive_time', methods=['POST'])
def return_node_alive_time():
    json_data = request.get_json()
    node_id = json_data['NodeID']
    #TODO: how to access node attributes??? same shit for all other attributes
    retrun 0

@app.route('sanushost/api/v1.0/check_aws_avg_time', methods=['GET'])
def retrun_aws_avg_time():


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')