import os, sys
sys.path.append(os.path.abspath('..'))
from sanus_face_server.mongo import mongo_client
import numpy as np
import pickle
# import boto3 
import socket


class IdClient():
    def __init__(self):
        self.EUC_THRESH = 1.0
        self.TIME_THRESH = 30 
        self.mongo_client = mongo_client.MongoClient('Sanus')

    def cosine_similarity(self, emb1, emb2):
        return np.dot(emb1, emb2)/(np.sqrt(np.sum(np.square(emb1))*np.sum(np.square(emb2))))

    def euclidean_distance(self, emb1, emb2):
        return np.linalg.norm(emb1 - emb2)

    def add_staff(self, embs, id):
        try:
            for index, emb in enumerate(embs):
                if index:
                    self.mongo_client.add_staff({'Name': id+str(index), 'Embedding': emb.tolist()})
                else:
                    self.mongo_client.add_staff({'Name': id, 'Embedding': emb.tolist()})
            return "Success"
        except:
            return "Failed"

    def remove_staff(self, id):
        try:
            self.mongo_client.remove_staff(id)
            return 'success'
        except:
            return 'failed'

    def check_staff(self, emb): 
        for staff in self.mongo_client.find_all():
            euc_dist = self.euclidean_distance(emb, np.asarray(staff['Embedding']))
            if euc_dist < self.EUC_THRESH:
                return (staff['Name'], 1)
        return (None, 0)