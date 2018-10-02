import requests
import numpy as np
import os, sys
sys.path.append(os.path.abspath('..'))
import base64
import ast
import time
from sanus_face_server.config import config

#TODO: how do we take the pic, laptop webcam or rpi????
class AddFaceClient():
    def __init__(self):
        self.host = config.SERVER_HOST
        self.port = config.SERVER_PORT
        self.url = 'http://' + self.host + ':' + self.port + '/sanushost/api/v1.0/add_face_img'
        self.node_type = 'add'
        self.
