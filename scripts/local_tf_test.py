"""
Local tf testing ground without serving

Author: Hongrui Zheng, Sanus Solutions
"""

from __future__ import print_function
import os, sys
import tensorflow as tf
import scipy.misc
import dlib
import numpy as np
from tensorflow.python.framework.tensor_util import MakeNdarray

def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1/std_adj)
    return y  

#TODO: generalize
ckpt_file = '/home/billyzheng/sanus_face_server/model/20170512-110547/model-20170512-110547.ckpt-250000'
meta_file = '/home/billyzheng/sanus_face_server/model/20170512-110547/model-20170512-110547.meta'

cnn_detector = dlib.cnn_face_detection_model_v1('/home/billyzheng/sanus_face_server/model/mmod_human_face_detector.dat')
sp = dlib.shape_predictor('/home/billyzheng/sanus_face_server/model/shape_predictor_5_face_landmarks.dat')
image = dlib.load_rgb_image('/home/billyzheng/Downloads/luka.jpeg')
dets = cnn_detector(image, 1)
faces = dlib.full_object_detections()
for detection in dets:
    faces.append(sp(image, detection.rect))
faces_list = np.asarray(dlib.get_face_chips(image, faces, 160), dtype=np.float64)
faces_list_w = []
for face in faces_list:
    faces_list_w.append(prewhiten(face))
faces_list_w_stack = np.stack(faces_list_w)

image2 = dlib.load_rgb_image('/home/billyzheng/Downloads/klausz.jpeg')
dets2 = cnn_detector(image2, 1)
faces2 = dlib.full_object_detections()
for detection2 in dets2:
    faces2.append(sp(image2, detection2.rect))
faces_list2 = np.asarray(dlib.get_face_chips(image2, faces2, 160), dtype=np.float64)
faces_list2 = prewhiten(faces_list2)

with tf.Session(graph=tf.Graph()) as sess:
    # tf.import_graph_def(graph_def, name='')
    saver = tf.train.import_meta_graph(meta_file, input_map=None)
    # sess.run(tf.global_variables_initializer())
    # sess.run(tf.local_variables_initializer())
    saver.restore(sess, ckpt_file)
    print("model restored.")
    g = tf.get_default_graph()
    print('graph got')
    img_in = g.get_tensor_by_name('input:0')
    phase_train_in = g.get_tensor_by_name('phase_train:0')
    embeddings_out = g.get_tensor_by_name('embeddings:0')
    print('tensors got')

    feed_dict1 = {img_in: faces_list_w_stack, phase_train_in:False}
    emb1 = sess.run(embeddings_out, feed_dict=feed_dict1)
    np.save('demo_luka_emb.npy', emb1)
    feed_dict2 = {img_in: faces_list2, phase_train_in:False}
    emb2 = sess.run(embeddings_out, feed_dict=feed_dict2)
    np.save('demo_klaus_emb.npy', emb2)

for emb in emb1:
    print(np.sqrt(np.sum(np.square(np.subtract(emb, emb2)))))