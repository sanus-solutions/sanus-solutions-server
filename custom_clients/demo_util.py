import numpy as np
import time

EUC_THRESH = 1.0
TIME_THRESH = 30.0

KLAUS_EMB = np.load('demo_klaus_emb.npy')
LUKA_EMB = np.load('demo_luka_emb.npy')
KIRK_EMB = np.load('demo_kirk_emb.npy')
SEMEON_EMB = np.load('demo_semeon_emb.npy')


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
    current_time = time.time()
    euc_dist_klaus = euclidean_distance(emb, KLAUS_EMB)
    euc_dist_luka = euclidean_distance(emb, LUKA_EMB)
    euc_dist_kirk = euclidean_distance(emb, KIRK_EMB)
    euc_dist_semeon = euclidean_distance(emb, SEMEON_EMB)
    print('klaus dist: ' + str(euc_dist_klaus) + ', luka dist: ' + str(euc_dist_luka) +
        ', kirk dis:' + str(euc_dist_kirk) + ', semeon dis:' + str(euc_dist_semeon))
    if (euc_dist_klaus < EUC_THRESH):
        #print ("Klaus' face detection took: %f s\n", time.time()-current_time)
        return (True, "klaus")
    elif (euc_dist_luka < EUC_THRESH):
        #print ("Luka's face detection took: %f s\n", time.time()-current_time)
        return (True, "luka")
    elif (euc_dist_kirk < EUC_THRESH):
        #print ("kirk's face detection took: %f s\n", time.time()-current_time)
        return (True, "kirk")
    elif (euc_dist_semeon < EUC_THRESH):
        #print ("simeon's face detection took: %f s\n", time.time()-current_time)
        return (True, "simeon")
    else:
        #print ("Face belongs to no one in database or other errors, took: %f s\n", time.time()-current_time)
        return (False, "None")
