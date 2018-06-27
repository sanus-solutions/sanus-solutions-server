"""
Exporting an existing .pb file for tf serving

Usage: export_model.py [protobuf dir] [export dir]

Author: Hongrui Zheng, Sanus Solutions
"""

from __future__ import print_function
import os, sys
import tensorflow as tf
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import tag_constants

pb_path = sys.argv[1]
export_path = sys.argv[2]

builder = tf.saved_model.builder.SavedModelBuilder(export_path)
with tf.gfile.GFile(pb_path, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
sigs = {}

with tf.Session(graph=tf.Graph()) as sess:
    tf.import_graph_def(graph_def, name='')
    g = tf.get_default_graph()
    img_in = g.get_tensor_by_name('input:0')
    phase_train_in = g.get_tensor_by_name('phase_train:0')
    embeddings_out = g.get_tensor_by_name('embeddings:0')
    sigs[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY] = \
        tf.saved_model.signature_def_utils.predict_signature_def(
            {'in': img_in, 'phase': phase_train_in}, {'out': embeddings_out})
    builder.add_meta_graph_and_variables(sess,
                                         [tag_constants.SERVING],
                                         signature_def_map=sigs)
builder.save()