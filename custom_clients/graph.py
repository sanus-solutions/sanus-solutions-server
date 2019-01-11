from pymongo import MongoClient
from sanus_face_server.config import config

class Graph():
    """
    Nodes in graph has:
        id, list of neighbors, list of latest ts, list of latest emb
    """

    def __init__(self, id_client):
        self.client = MongoClient(config.MONGO_HOST, config.MONGO_PORT)
        self.db = self.client[config.MONGO_DB_NAME]
        self.collection = self.db[config.MONGO_DB_COL]

    def add_node(self, name, n):
        # TODO: automatically finds the neighbors?
        # add a node in the graph with id and neighbors, ts and emb empty
        # name: int id
        # neighbors: list of int ids
        # returns 0 if success
        
        # check if node exists
        current_count = self.collection.count({id: name})
        # count should be either 1 or 0
        if !current_count:
            # no previous record
            new_node = {id: name, neighbors: n, timestamps: [], embeddings:[]}
            self.collection.insert(new_node)
            return 0
        else:
            # previous record exists, merge the neighbors
            rec = self.collection.find({id: name})
            new_neighbors = set(rec['neighbors'] + n)
            self.collection.update_one({id: name}, {'$set': {neighbors: new_neighbors}})
            return 0

        return 'lolshit'

    def remove_node(self, name):
        self.collection.delete_one({id: name})
        return 0

    def update_node(self, name, embedding, timestamp):
        rec = self.collection.find({id: name})
        new_timestamps = rec['timestamps'].append(timestamp)
        new_embeddings = rec['embeddings'].append(embedding)
        self.collection.update_one({id: name}, {"$set": {timestamps: new_timestamps, embeddings: new_embeddings}})
        return 0

    def check_breach(self, embeddings, timestamp, location):
        return 0

