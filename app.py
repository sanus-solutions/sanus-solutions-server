from __future__ import print_function
import numpy as np
from custom_clients import tf_serving_client, graph
from custom_clients import image_preprocessor, image_preprocessor_dlib
from flask import Flask, request
import sys, json, base64
import tensorflow as tf
from scipy import misc


app = Flask(__name__)
serving_client = tf_serving_client.TFServingClient()
dlib_preprocessor = image_preprocessor_dlib.DlibPreprocessor()
with tf.Graph().as_default():
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=config.GPU_FRACTION)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
    with sess.as_default():
        pnet, rnet, onet = image_preprocessor.create_mtcnn(sess, None)

"""
route for adding node in graph
request payload format:
{'Location': location, 'Type': node_type}
"""
@app.route('/sanushost/api/v1.0/add_node', methods=['POST'])
def add_node():
    json_data = request.get_json()
    location = json_data['Location']
    node_type = json_data['Type']
    result = graph.add_node(location, node_type)
    return json.dumps({'Status': result})

"""
route for removing node in graph
request payload format:
{'Location': location, 'Type': node_type}
"""
@app.route('/sanushost/api/v1.0/remove_node', methods=['POST'])
def remove_node():
    json_data = request.get_json()
    location = json_data['Location']
    node_type = json_data['Type']
    result = graph.remove_node(location, node_type)
    return json.dumps({'Status': result})

"""
route for sanitizer clients
request payload format:
{'Timestamp': tiemstamp, 'Location': location, 'Image': image_64str}
"""
@app.route('/sanushost/api/v1.0/sanitizer_img', methods=['POST'])
def receive_sanitizer_image():
    json_data = request.get_json()
    image_str = json_data['Image']
    timestamp = json_data['Timestamp']
    location = json_data['Location']
    image = np.frombuffer(base64.decodestring(image_str), dtype=np.float64)
    if config.USE_DLIB:
        image_preprocessed = dlib_preprocessor.process(image)
    elif config.USE_MTCNN:
        img_list = []
        img_size = np.asarray(image.shape)[0:2]
        margin = config.MARGIN
        image_size = config.IMAGE_SIZE
        bbox, _ = image_preprocessor.detect_face(image, config.MIN_SIZE, pnet, rnet, onet, config.MTCNN_THRESHOLD, config.MTCNN_FACTOR)
        if len(bbox) < 1:
            return json.dumps({'Status': 'No Face'})
        det = np.squeeze(bbox[0, 0:4])
        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0]-margin/2, 0)
        bb[1] = np.maximum(det[1]-margin/2, 0)
        bb[2] = np.minimum(det[2]+margin/2, img_size[1])
        bb[3] = np.minimum(det[3]+margin/2, img_size[0])
        cropped = image[bb[1]:bb[3],bb[0]:bb[2],:]
        aligned = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
        prewhitened = image_preprocessor.prewhiten(aligned)
        img_list.append(prewhitened)
        image_preprocessed = np.stack(img_list)
    # TODO: preprocessed image is list of face chips
    # TODO: None if no faces detected
    # TODO: enable batch inference, fail mechanism
    embeddings = serving_client.send_inference_request(image_preprocessed)
    # TODO: add embedding to graph with timestamp and location
    result = graph.add_to_graph(embeddings, timestamp, location)
    return json.dumps({'Status': result})

"""
route for entry clients
request payload format:
{'Timestamp': tiemstamp, 'Location': location, 'Image': image_64str}
"""
@app.route('/sanushost/api/v1.0/entry_img', methods=['POST'])
def receive_entry_image():
    json_data = request.get_json()
    image_str = json_data['Image']
    timestamp = json_data['Timestamp']
    location = json_data['Location']
    image = np.frombuffer(base64.decodestring(image_str), dtype=np.float64)
    if config.USE_DLIB:
        image_preprocessed = dlib_preprocessor.process(image)
    elif config.USE_MTCNN:
        img_list = []
        img_size = np.asarray(image.shape)[0:2]
        margin = config.MARGIN
        image_size = config.IMAGE_SIZE
        bbox, _ = image_preprocessor.detect_face(image, config.MIN_SIZE, pnet, rnet, onet, config.MTCNN_THRESHOLD, config.MTCNN_FACTOR)
        if len(bbox) < 1:
            return json.dumps({'Status': 'No Face'})
        det = np.squeeze(bbox[0, 0:4])
        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0]-margin/2, 0)
        bb[1] = np.maximum(det[1]-margin/2, 0)
        bb[2] = np.minimum(det[2]+margin/2, img_size[1])
        bb[3] = np.minimum(det[3]+margin/2, img_size[0])
        cropped = image[bb[1]:bb[3],bb[0]:bb[2],:]
        aligned = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
        prewhitened = image_preprocessor.prewhiten(aligned)
        img_list.append(prewhitened)
        image_preprocessed = np.stack(img_list)
    # TODO: preprocessed image is list of face chips
    # TODO: None if no faces detected
    # TODO: enable batch inference, fail mechanism
    embeddings = serving_client.send_inference_request(image_preprocessed)
    # TODO: do graph search and compare here, determine if breach happend
    result = graph.check_breach(embeddings, timestamp, location)
    return json.dumps({'Status': result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')