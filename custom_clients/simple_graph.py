import os, sys
sys.path.append(os.path.abspath('..'))
import numpy as np
import time
from sanus_face_server.custom_clients import id_client
import collections
import boto3

"""
minimal implementation of graph structure
"""
class SimpleGraph():
    """
    underlying data structure saved in self.node_list
    node_list is a dictionary with node_id as key and info of node as value
    node info is a dictionary with neighbors, node type, latest embeddings, and latest timestamp
    """
    def __init__(self, id_client):
        self.node_list = {}
        self.time_thresh = 100 # seconds
        self.dist_thresh = 0.15 # TODO: what's a good similarity threshold here????
        # self.id_client = id_client.IdClient()
        self.id_client = id_client

        # DEMO USES ONLY ATTRIBUTES BELOW
        # self.demo_node_list = {
        # 'demo_sanitizer': 
        #     {'neighbors': ['demo_entry'], 'node_type': 'san', 'embeddings': collections.deque(maxlen=10), 'timestamp': collections.deque(maxlen=10)}, 
        # 'demo_entry':
        #     {'neighbors': ['demo_entry'], 'node_type': 'ent', 'embeddings': collections.deque(maxlen=10), 'timestamp': collections.deque(maxlen=10)}
        # }
        self.demo_node_list = {}

    # DEMO USES ONLY METHODS BELOW
    def demo_check_breach(self, embeddings, timestamp):
        for idx, emb in enumerate(embeddings):
            staff = self.id_client.check_staff(emb)
            if staff[0]:
                time_diff = 0
                for node_id in self.demo_node_list:
                    node_emb_list = self.demo_node_list[node_id]['embeddings']
                    node_timestamp_list = self.demo_node_list[node_id]['timestamp']

                    for index, node_timestamp in enumerate(node_timestamp_list):
                        time_diff = abs(node_timestamp - timestamp)
                        print(time_diff)
                        if time_diff < self.id_client.TIME_THRESH + 19: # Offset time difference
                            if self.euclidean_distance(node_emb_list[index], emb) < self.id_client.EUC_THRESH:
                                return True, staff[1]
                        else:
                            #print(self.demo_node_list[node_id], type(self.demo_node_list[node_id]))
                            #print(node_emb_list[index], type(node_emb_list[index]))
                            self.demo_node_list[node_id]['embeddings'].remove(node_emb_list[index])
                            self.demo_node_list[node_id]['timestamp'].remove(node_timestamp)
                            print(str(node_id) + " is removed from collection")
                return False, staff[1]

                # node_emb_list = self.demo_node_list['demo_sanitizer']['embeddings']
                # timestamp_list = self.demo_node_list['demo_sanitizer']['timestamp']
                # for node_idx, node_emb in enumerate(node_emb_list):
                #     if self.euclidean_distance(node_emb, emb) < self.id_client.EUC_THRESH:
                #         time_diff = abs(timestamp - timestamp_list[node_idx])
                #         #print('found person in sanitizer list', time_diff)
                #         return time_diff < self.id_client.TIME_THRESH, staff[1]
                #     else:
                #         continue
                # return False, staff[1]
            else:
                #print("None staff's face detected")
                return False, None

    def demo_update_node(self, embeddings, timestamp, node_id):
        # try:
        #     for i in range(9):
        #         ## Hard code
        #         self.demo_node_list['demo_sanitizer']['embeddings'].appendleft(embeddings[i])
        #         self.demo_node_list['demo_sanitizer']['timestamp'].appendleft(timestamp)
        #         # self.demo_node_list[node_id]['embeddings'].appendleft(embeddings[i])
        #         # self.demo_node_list[node_id]['timestamp'].appendleft(timestamp)
        #print(self.demo_node_list)    staff_id = graph.demo_check_staff(embeddings)
        try:
            self.demo_node_list[node_id]['embeddings'].append(embeddings[0])
            self.demo_node_list[node_id]['timestamp'].append(timestamp)
            #print(node_id + ' updated at time: ' + str(timestamp))
        except:
            self.demo_node_list[node_id] = {'embeddings' : [embeddings[0]], 'timestamp' : [timestamp]}
            #print(node_id + ' created at time: ' + str(timestamp))
        #print(self.demo_node_list)

    def demo_check_staff(self, embeddings):
        for idx, emb in enumerate(embeddings):
            staff = self.id_client.check_staff(emb)
            if staff[0]:
                return str(staff[1])
            else:
                return 'None Staff'

    """loss metrics"""
    def cosine_similarity(self, emb1, emb2):
        return np.dot(emb1, emb2)/(np.sqrt(np.sum(np.square(emb1))*np.sum(np.square(emb2))))

    def euclidean_distance(self, emb1, emb2):
        # return 1 - np.sqrt(np.sum(np.square(emb1 - emb2)))
        return np.linalg.norm(emb1 - emb2)

    """graph utilities"""
    def add_node(self, node_id, neighbors, node_type, embeddings=None, timestamp=None):
        """
        node_id should be a string
        neighbors should be list of node_id strings
        node_type should be a string
        embeddings and timestamp default to None
        """
        try:    
            staff_id = graph.demo_check_staff(embeddings)
            temp = self.node_list[node_id]
            #print('Node exists, with neighbors: ' + str(temp['neighbors']) + 'and type ' + temp['node_type'])
            return 0
        except KeyError:
            #print('Adding node now.')
            self.node_list[node_id] = {'neighbors': neighbors, 'node_type': node_type, 'embeddings': embeddings, 'timestamp': timestamp}
            self.update_neighbors(node_id, neighbors)
            return 1

    def remove_node(self, node_id):
        status = self.node_list.pop(node_id, 0)
        if status == 0:
            #print('node removal failed, node_id given was not in the graph.')
            return 0
        else:
            return 1
