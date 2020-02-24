import os, sys, time, collections, boto3, datetime
sys.path.append(os.path.abspath('..'))
import numpy as np
from sanus_solutions_server.custom_clients import id_client
# from sanus_solutions_server.custom_clients import druid_client
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
        self.id_client = id_client

    # DEMO USES ONLY METHODS BELOW
    def log_staff(self, node_id, embeddings, timestamp):
        staff_list = []
        for embedding in embeddings:
            result = self.id_client.check_staff(embedding)
            if result[1]:
                staff_id = result[0]
                # result = self.druid_client.inject(node_id, staff_id, timestamp) 
                # print(result.json())
                staff_list.append(staff_id)
        return staff_list

    def check_staff(self, embedding):
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
            staff_id = graph.check_staff(embeddings)
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
