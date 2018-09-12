import numpy as np
import pickle
# TODO import file with face collection data structure


class IdClient():
    def __init__(self):
        self.EUC_THRESH = 1.0
        with open('face_collection.pkl', 'rb') as f:
            self.face_collection = pickle.load(f)
    def cosine_similarity(self, emb1, emb2):
        return np.dot(emb1, emb2)/(np.sqrt(np.sum(np.square(emb1))*np.sum(np.square(emb2))))

    def euclidean_distance(self, emb1, emb2):
        return np.linalg.norm(emb1 - emb2)

    def add_staff(self, emb, id):
        self.face_collection[id] = emb
        with open('face_collection.pkl', 'wb') as f:
            pickle.dump(self.face_collection, f)

    def check_staff(self, emb):
        for staff_id in self.face_collection:
            euc_dist = euclidean_distance(emb, self.face_collection[staff_id])
            if euc_dist < EUC_THRESH:
                return (True, staff_id)
            return (False, '')

