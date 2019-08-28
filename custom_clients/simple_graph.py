import os, sys, time, collections, boto3, datetime
sys.path.append(os.path.abspath('..'))
import numpy as np
from sanus_face_server.custom_clients import id_client
from sanus_face_server.mongo import mongo_hygiene_client
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

        ## A temporary 
        self.hygiene_record = mongo_hygiene_client.MongoClient()

    # DEMO USES ONLY METHODS BELOW
    def check_breach(self, embeddings, timestamp):
        check_breach_time_start = time.time()
        staff_list = []
        for idx, emb in enumerate(embeddings):
            ## check_staff returns 
            ## (name, 1) if staff exits
            ## (none, 0) 
            staff = self.id_client.check_staff(emb)
            if staff[1]:
                current_staff_records = self.hygiene_record.find('Staff', staff[0])
                if current_staff_records.count(): 
                    for record in current_staff_records:
                        current_timestamp = datetime.datetime.fromtimestamp(timestamp).replace(tzinfo=datetime.timezone.utc)
                        time_diff = abs((record['Timestamp'].replace(tzinfo=datetime.timezone.utc) - current_timestamp).total_seconds())
                        if time_diff < self.id_client.TIME_THRESH: 
                            staff_list.append((staff[0], 1)) # (Name, Clean)
                            break
                else:
                    staff_list.append((staff[0], 0)) # (Name, Not clean)
            else:
                ## None staff
                staff_list.append((None, 0)) # (No name, Not clean)
        return staff_list

    def check_breach_by_name(self, staff_list, timestamp):
        result = []
        for staff in staff_list:
            current_staff_result = (staff, 0) # (Name, Not clean), default not clean
            current_staff_records = self.hygiene_record.find('Staff', staff)
            if current_staff_records.count(): 
                for record in current_staff_records:
                    current_timestamp = datetime.datetime.fromtimestamp(timestamp).replace(tzinfo=datetime.timezone.utc)
                    time_diff = abs((record['Timestamp'].replace(tzinfo=datetime.timezone.utc) - current_timestamp).total_seconds())
                    if time_diff < self.id_client.TIME_THRESH: 
                        current_staff_result = (staff, 1) # Replace by 'clean'

            result.append(current_staff_result)
        return result

    def update_node(self, embeddings, timestamp, node_id):
        for emb in embeddings:
            staff = self.id_client.check_staff(emb)
            if staff[1]:
                ## Remove this try statement later. Node_ID shall exit when a new dispenser unit is added to the location based graph
                ## Convert to utc
                timestamp = datetime.datetime.fromtimestamp(timestamp).replace(tzinfo=datetime.timezone.utc)
                current_dictionary = {
                'NodeID' : node_id,
                'Timestamp' : timestamp,
                'Staff' : staff[0],
                }
                try:
                    return self.hygiene_record.insert_record(current_dictionary).acknowledged
                except:
                    ## TODO
                    return False
        return False

    def check_staff(self, embeddings):
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
