"""
Exporting trained model (meta graph and variables) for tf serving

Usage: export_model.py [model dir] [export dir]

Author: Hongrui Zheng, Sanus Solutions
"""

from __future__ import print_function
import os, sys
import tensorflow as tf
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import tag_constants

model_path = sys.argv[1]
export_path = sys.argv[2]

builder = tf.saved_model.builder.SavedModelBuilder(export_path)
# with tf.gfile.GFile(model_path+pb_path, 'rb') as f:
#     graph_def = tf.GraphDef()
#     graph_def.ParseFromString(f.read())
sigs = {}

#TODO: generalize
ckpt_file = '/home/billyzheng/sanus_face_server/model/20170512-110547/model-20170512-110547.ckpt-250000'
meta_file = '/home/billyzheng/sanus_face_server/model/20170512-110547/model-20170512-110547.meta'

with tf.Session(graph=tf.Graph()) as sess:
    # tf.import_graph_def(graph_def, name='')
    saver = tf.train.import_meta_graph(meta_file, input_map=None)
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())
    saver.restore(sess, ckpt_file)
    print("model restored.")
    g = tf.get_default_graph()
    print('graph got')
    img_in = g.get_tensor_by_name('input:0')
    phase_train_in = g.get_tensor_by_name('phase_train:0')
    embeddings_out = g.get_tensor_by_name('embeddings:0')
    print('tensors got')
    sigs[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY] = \
        tf.saved_model.signature_def_utils.predict_signature_def(
            {'in': img_in, 'phase': phase_train_in}, {'out': embeddings_out})
    print('sigs done')
    builder.add_meta_graph_and_variables(sess,
                                         [tag_constants.SERVING],
                                         signature_def_map=sigs)
    print('graph var added')
builder.save()
print('saved shit')