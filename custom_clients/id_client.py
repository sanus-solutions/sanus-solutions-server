import os, sys
sys.path.append(os.path.abspath('..'))
from sanus_face_server.mongo import mongo_face_client
import numpy as np
# import boto3 
import socket


class IdClient():
    def __init__(self,):
        self.EUC_THRESH = 1.0
        self.TIME_THRESH = 30 
        self.mongo_client = mongo_face_client.MongoClient()

    def cosine_similarity(self, emb1, emb2):
        return np.dot(emb1, emb2)/(np.sqrt(np.sum(np.square(emb1))*np.sum(np.square(emb2))))

    def euclidean_distance(self, emb1, emb2):
        return np.linalg.norm(emb1 - emb2)

    def add_staff(self, embs, id):
        ## NEED TO REWORK 
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
        ## NEED TO RE WORK
        result = self.mongo_client.remove_staff(id)
        if result:
            if result.raw_result['n']:
                return "Success"
            else:
                return "No such staff found"
        return "Failed"


    def check_staff(self, emb): 
        for staff in self.mongo_client.find_all():
            euc_dist = self.euclidean_distance(emb, np.asarray(staff['Embedding']))
            if euc_dist < self.EUC_THRESH:
                return (staff['Name'], 1)
        return (None, 0)