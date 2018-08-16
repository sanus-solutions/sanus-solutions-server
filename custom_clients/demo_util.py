import numpy as np

EUC_THRESH = 1.0

KLAUS_EMB = np.load('demo_klaus_emb.npy')
LUKA_EMB = np.load('demo_luka_emb.npy')

def cosine_similarity(emb1, emb2):
        return np.dot(emb1, emb2)/(np.sqrt(np.sum(np.square(emb1))*np.sum(np.square(emb2))))

def euclidean_distance(emb1, emb2):
    # return 1 - np.sqrt(np.sum(np.square(emb1 - emb2)))
    return np.linalg.norm(emb1 - emb2)

def l2_dist(emb1, emb2):
    d = (emb1 - emb2)
    return np.dot(d, d)

def dist(emb1, emb2):
    return np.sqrt(np.sum(np.square(np.subtract(emb1, emb2))))

def check_staff(emb):
    euc_dist_klaus = euclidean_distance(emb, KLAUS_EMB)
    euc_dist_luka = euclidean_distance(emb, LUKA_EMB)
    print('klaus dist: ' + str(euc_dist_klaus) + ', luka dist: ' + str(euc_dist_luka))
    if (euc_dist_klaus < EUC_THRESH or euc_dist_luka < EUC_THRESH):
        return True
    else:
        return False
