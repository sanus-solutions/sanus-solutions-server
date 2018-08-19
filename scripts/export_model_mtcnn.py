"""
Exporting trained model (meta graph and variables) for tf serving

Usage: export_model_mtcnn.py [export dir]

Author: Hongrui Zheng, Sanus Solutions
"""

from __future__ import print_function
import os, sys
import tensorflow as tf
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import tag_constants

export_path = sys.argv[1]
model_path = '/home/billyzheng/sanus_face_server/model/mtcnn/mtcnn.pb'

builder = tf.saved_model.builder.SavedModelBuilder(export_path)
with tf.gfile.GFile(model_path, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
sigs = {}

#TODO: generalize
# ckpt_file = '/home/billyzheng/sanus_face_server/model/20170512-110547/model-20170512-110547.ckpt-250000'
# meta_file = '/home/billyzheng/sanus_face_server/model/20170512-110547/model-20170512-110547.meta'

with tf.Session(graph=tf.Graph()) as sess:
    tf.import_graph_def(graph_def, name='')
    print('graph imported')
    # saver = tf.train.import_meta_graph(meta_file, input_map=None)
    # sess.run(tf.global_variables_initializer())
    # sess.run(tf.local_variables_initializer())
    # saver.restore(sess, ckpt_file)
    # print("model restored.")
    g = tf.get_default_graph()
    print('graph got')
    # inputs

    img_in = g.get_tensor_by_name('input:0')
    min_size_in = g.get_tensor_by_name('min_size:0')
    thresholds_in = g.get_tensor_by_name('thresholds:0')
    factor_in = g.get_tensor_by_name('factor:0')
    # outputs
    prob_out = g.get_tensor_by_name('prob:0')
    lmk_out = g.get_tensor_by_name('landmarks:0')
    box_out = g.get_tensor_by_name('box:0')
    print('tensors got')

    sigs[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY] = \
        tf.saved_model.signature_def_utils.predict_signature_def(
            {'in': img_in, 'min_size': min_size_in, 'thresholds': thresholds_in, 'factor': factor_in},
            {'prob': prob_out, 'lmk': lmk_out, 'box': box_out})
    print('sigs done')
    builder.add_meta_graph_and_variables(sess,
                                         [tag_constants.SERVING],
                                         signature_def_map=sigs)
    print('graph var added')
builder.save()
print('saved shit')