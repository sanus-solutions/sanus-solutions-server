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
        staff_list = []
        for idx, emb in enumerate(embeddings):
            ## check_staff returns 
            ## (name, 1) if staff exits
            ## (none, 0) 
            staff = self.id_client.check_staff(emb)
            if staff[1]:
                time_diff = 0
                
                for node_id in self.demo_node_list:
                    node_emb_list = self.demo_node_list[node_id]['embeddings']
                    node_timestamp_list = self.demo_node_list[node_id]['timestamp']

                    ## Case1: don't find any record in the entire graph, 
                    ## current_staff_list is empty, insert (staff[0], 0)
                    ## Case2: find multiple records in the graph
                    ## break the search until the first clean record found insert (staff[0], 1)
                    ## otherwise insert (staff[0], 0)
                    ## Average searchtime: O(nm)
                    current_staff_list = []
                    for index, node_timestamp in enumerate(node_timestamp_list):
                        time_diff = abs(node_timestamp - timestamp)
                        if time_diff < self.id_client.TIME_THRESH: 
                            if self.euclidean_distance(node_emb_list[index], emb) < self.id_client.EUC_THRESH:
                                current_staff_list.append(staff[0], 1) # (Name, Clean)
                                break 
                        else:
                            #print(self.demo_node_list[node_id], type(self.demo_node_list[node_id]))
                            #print(node_emb_list[index], type(node_emb_list[index]))
                            self.demo_node_list[node_id]['embeddings'].remove(node_emb_list[index])
                            self.demo_node_list[node_id]['timestamp'].remove(node_timestamp)
                            #print(str(node_id) + " is removed from collection")
                            
                    if len(current_staff_list):
                        staff_list += current_staff_list
                    else:
                        staff_list.append(staff[0], 0) # (Name, Not clean)
            else:
                ## None staff
                staff_list.append((None, 0)) # (No name, Not clean)
        return staff_list

    def demo_update_node(self, embeddings, timestamp, node_id):
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
