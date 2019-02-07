from sanus_face_server.custom_clients import graph
import numpy as np
import time

# constants
NUM_TESTS = 100
LEN_EMB = 512

test_graph = graph.Graph()

# ADD/REMOVE NODE TESTS (empty neighb0rs)
# one node id test
str_id = 'dummy'
num_id = 8888
print('=====STARTING ADD NODE TEST======')
try:
    start_time = time.time()
    test_graph.add_node(str_id, [])
    duration = time.time() - start_time
    print('node id ' + str_id + 'added in :' + str(duration) + ' seconds.')
except e:
    print('failed: ' + str(e))

try:
    start_time = time.time()
    test_graph.add_node(num_id, [])
    duration = time.time() - start_time
    print('node id ' + str(num_id) + 'added in :' + str(duration) + ' seconds.')
except e:
    print('failed: ' + str(e))

# same node id test
# same node id, graph should merge the neighbors list

# adding empty neighbors again
try:
    print('adding node again with empty neighbors.')
    test_graph.add_node(str_id, [])
    rec = test_graph.collection.find({id: str_id})
    assert rec['neighbors'] == []
    print('new neighbors list: ' + rec['neighbors'])
except e:
    print('failed: ' + e)
# adding non-empty neighbors again
try:
    print('adding node again with non-empty neighbors.')
    test_graph.add_node(str_id, ['klausisadumbass', 'klausisstilladumbass'])
    rec = test_graph.collection.find({id: str_id})
    assert rec['neighbors'] == ['klausisadumbass', 'klausisstilladumbass']
    print('new neighbors list: ' + rec['neighbors'])
except e:
    print('failed: ' + e)
# add same neighbors list to test merging function
try:
    print('adding node again with non-empty repeating neighbors.')
    test_graph.add_node(str_id, ['klausisadumbass', 'klausisstilladumbass'])
    rec = test_graph.collection.find({id: str_id})
    assert rec['neighbors'] == ['klausisadumbass', 'klausisstilladumbass']
    print('new neighbors list: ' + rec['neighbors'])
except e:
    print('failed: ' + e)

# add intersecting neighbors lists to test merging function
try:
    print('adding node again with non-empty repeating neighbors.')
    test_graph.add_node(str_id, ['klausisadumbass', 'klausisstilladumbass', 'klausisagainadumbass'])
    rec = test_graph.collection.find({id: str_id})
    assert rec['neighbors'] == ['klausisadumbass', 'klausisstilladumbass', 'klausisagainadumbass']
    print('new neighbors list: ' + rec['neighbors'])
except e:
    print('failed: ' + e)

# add non-intersecting neighbors lists to test merging function
try:
    print('adding node again with non-empty repeating neighbors.')
    test_graph.add_node(str_id, ['nahklausstilldumb', 'headumbass'])
    rec = test_graph.collection.find({id: str_id})
    assert rec['neighbors'] == ['klausisadumbass', 'klausisstilladumbass', 'klausisagainadumbass', 'nahklausstilldumb', 'headumbass']
    print('new neighbors list: ' + rec['neighbors'])
except e:
    print('failed: ' + e)

# same test for number id may be necessary?
# try:
#     print('adding node again with empty neighbors.')
#     test_graph.add_node(num_id, [])
#     rec = test_graph.collection.find({id: num_id})
#     print('new neighbors list: ' + rec['neighbors'])
# except e:
#     print('failed: ' + e)

# try:
#     print('adding node again with non-empty neighbors.')
#     test_graph.add_node(num_id, ['klausisadumbass', 'klausisstilladumbass'])
#     rec = test_graph.collection.find({id: num_id})
#     print('new neighbors list: ' + rec['neighbors'])
# except e:
#     print('failed: ' + e)

# no node id test


# REMOVE NODE TESTS
# r

# random tests
rand_embs_to_add = np.rand(NUM_TESTS, LEN_EMB)
for row in rand_embs_to_add:
    test_graph.add_node()