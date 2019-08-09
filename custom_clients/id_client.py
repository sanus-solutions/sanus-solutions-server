import os, sys
sys.path.append(os.path.abspath('..'))
from sanus_face_server.mongo import mongo_face_client
import numpy as np
# import boto3 
import socket
# Serial generator
import string, random
# Logger
import logging, time

class IdClient():
    def __init__(self,):
        self.EUC_THRESH = 1.0
        self.TIME_THRESH = 30 
        self.mongo_client = mongo_face_client.MongoClient()

        ## Logger 
        level = self.log_level(logging.DEBUG)
        self.logger = logging.getLogger('IdClient')
        self.logger.setLevel(level)

        ## Temporary streamhandler for debug 
        ch = logging.FileHandler("IdClient.log")

        ch.setLevel(level)
        formatter = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def cosine_similarity(self, emb1, emb2):
        return np.dot(emb1, emb2)/(np.sqrt(np.sum(np.square(emb1))*np.sum(np.square(emb2))))

    def euclidean_distance(self, emb1, emb2):
        return np.linalg.norm(emb1 - emb2)

    def add_staff(self, embs, id):
        ## NEED TO REWORK 
        try:
            for index, emb in enumerate(embs):
                if index:
                    self.mongo_client.add_staff({'Staff': id+str(index), 'Embedding': emb.tolist()})
                else:
                    self.mongo_client.add_staff({'Staff': id, 'Embedding': emb.tolist()})
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
        start_time = time.time()
        counter = 0
        for staff in self.mongo_client.find_all():
            counter += 1
            euc_dist = self.euclidean_distance(emb, np.asarray(staff['Embedding']))
            if euc_dist < self.EUC_THRESH:
                self.logger.debug("Embedding is found in database, took %s iteration in %s seconds.", 
                    str(counter), 
                    str(time.time() - start_time))
                return (staff['Staff'], 1)

        ## Generate random id and add new face embedding to library        
        self.add_staff(emb, self.generate_serial())
        self.logger.debug("Embedding is not found in databse, took %s iteration in %s seconds. New embedding is added to database.", 
            str(counter),
            str(time.time() - start_time))
        return (None, 0)

    def generate_serial(self, size=9):
        chars=string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for i in range(size))
