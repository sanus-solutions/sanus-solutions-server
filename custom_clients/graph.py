from pymongo import MongoClient
import numpy as np
import time
from sanus_face_server.config import config


class Graph():
    """
    Nodes in graph has:
        id, list of neighbors, list of latest ts, list of latest emb
    """

    def __init__(self):
        self.client = MongoClient(config.MONGO_HOST, config.MONGO_PORT)
        self.db = self.client[config.MONGO_DB_NAME]
        self.collection = self.db[config.MONGO_DB_COL]
        self.staff_collection = self.db['staff']

        # constants
        self.EUC_THRESH = 1.0
        self.TIME_THRESH = 30.0

    def add_node(self, name, n):
        # TODO: automatically finds the neighbors?
        # add a node in the graph with id and neighbors, ts and emb empty
        # name: int id
        # neighbors: list of int ids        
        # check if node exists
        current_count = self.collection.count({id: name})
        # count should be either 1 or 0
        if current_count != 0 || current_count != 1:
            return 'failed'
        if !current_count:
            # no previous record
            try:
                new_node = {id: name, neighbors: n, timestamps: [], embeddings:[]}
                self.collection.insert(new_node)
                return 'success'
            except:
                return 'failed'
        else:
            # previous record exists, merge the neighbors
            try:
                rec = self.collection.find({id: name})
                new_neighbors = set(rec['neighbors'] + n)
                self.collection.update_one({id: name}, {'$set': {neighbors: new_neighbors}})
                return 'success'
            except:
                return 'failed'


    def remove_node(self, name):
        try:
            self.collection.delete_one({id: name})
            return 'success'
        except:
            return 'failed'

    def add_staff(self, emb, name):
        # staff should be stored in a separate collection
        try:
            new_staff = {id: name, embedding: emb}
            self.staff_collection.insert(new_staff)
            return 'success'
        except:
            return 'failed'

    def check_staff(self, emb):
        for rec in self.staff_collection.find():
            dist = self.euclidean_distance(rec['embeddings'], emb)
            if dist < self.EUC_THRESH:
                return (True, rec['id'])
        return (False, None)

    def remove_staff(self, name):
        try:
            self.staff_collection.delete_one({id: name})
            return 'success'
        except:
            return 'failed'

    def update_node(self, name, embedding, timestamp):
        try:
            rec = self.collection.find({id: name})
            new_timestamps = rec['timestamps'].append(timestamp)
            new_embeddings = rec['embeddings'].append(embedding)
            self.collection.update_one({id: name}, {"$set": {timestamps: new_timestamps, embeddings: new_embeddings}})
            return 'success'
        except:
            return 'failed'

    def check_breach(self, embeddings, timestamp, id):
        # TODO: how many depths to check? Only immediate neighbors?
        # first check staff, if not staff, no breach
        # there should only be one record under the id
        current_time = time.time()
        # check if staff
        staff, id = self.check_staff(embeddings)
        if !staff:
            return False, None
        rec = self.collection.find({name: id})
        for neighbor in rec['neighbors']:
            for idx, emb in enumerate(self.collection.find({name: neighbor})['embeddings']):
                if self.distance(emb, embeddings) < self.EUC_THRESH:
                    time_diff = abs(timestamp - self.collection.find({name: neighbor})['timestamps'][idx])
                    return time_diff < self.TIME_THRESH, id
                else:
                    continue
        return 0



    # helpers
    def distance(self, emb1, emb2):
        return np.linalg.norm(emb1 - emb2)