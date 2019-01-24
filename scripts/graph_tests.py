from sanus_face_server.custom_clients import graph
import numpy as np

# constants
NUM_TESTS = 100
LEN_EMB = 512

test_graph = graph.Graph()

# same node id test

# no node id test


# random tests
rand_embs_to_add = np.rand(NUM_TESTS, LEN_EMB)
for row in rand_embs_to_add:
    test_graph.add_node()