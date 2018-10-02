import numpy as np
import pickle
# TODO import file with face collection data structure


class IdClient():
    def __init__(self):
        self.EUC_THRESH = 1.0
        try:
            with open('face_collection.pkl', 'rb') as f:
                self.face_collection = pickle.load(f)
            print('face collection loaded')
        except:
            with open('face_collection.pkl', 'wb') as f:
                self.face_collection = {}
                pickle.dump(dict(), f)
            print('new face collection created')
    def cosine_similarity(self, emb1, emb2):
        return np.dot(emb1, emb2)/(np.sqrt(np.sum(np.square(emb1))*np.sum(np.square(emb2))))

    def euclidean_distance(self, emb1, emb2):
        return np.linalg.norm(emb1 - emb2)

    def add_staff(self, emb, id):
        self.face_collection[id] = emb
        try:
            with open('face_collection.pkl', 'wb') as f:
                pickle.dump(self.face_collection, f)
                return 'success'
        except:
            return 'failed'

    def remove_staff(self, id):
        self.face_collection.pop(id)
        try:
            with open('face_collection.pkl', 'wb') as f:
                pickle.dump(self.face_collection, f)
                return 'success'
        except:
            return 'failed'

    def check_staff(self, emb):
        for staff_id in self.face_collection:
            euc_dist = self.euclidean_distance(emb, self.face_collection[staff_id])
            if euc_dist < self.EUC_THRESH:
                return (True, staff_id)
            return (False, '')

