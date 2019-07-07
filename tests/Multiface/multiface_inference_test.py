import configparser,logging,


import requests
import numpy as np
from PIL import Image
import base64
import ast
import time
import json 


try: 
    config = configparser.ConfigParser()
    config.read('config.ini')
except:
    raise Exception("config.ini file not found.")

class MultifaceInferenceTest():
	def __init__(self, ):
		## Logger
		level = self.log_level(config.get('DEFAULT', 'LogLevel'))
        self.logger = logging.getLogger(config.get('DEFAULT', 'Name'))
        self.logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def log_level(self, level):
    	## if level doesn't match any, return DEBUG
        if level == 'INFO':
            return logging.INFO
        elif level == 'DEBUG':
        	return logging.DEBUG
        elif level == 'WARNING':
            return logging.WARNING
        elif level == 'ERROR':
        	return logging.ERROR
        elif level == 'CRITICAL':
        	return logging.CRITICAL
        else:
        	return logging.DEBUG
    
    def load_photos(self, path):








		url = 'http://192.168.0.101:5000/sanushost/api/v1.0/entry_img2'

		image = np.asarray(Image.open('luka.png'), dtype=np.uint8)


		shape_string = str(image.shape)
		print(shape_string)
		image = image.astype(np.float64)
		# image_temp = np.reshape(image, (1, image.shape[0]*image.shape[1]*image.shape[2]))
		img_64 = base64.b64encode(image).decode('ascii')
		# payload = {"NodeID": "demo_sanitizer", "Timestamp": [time.time()], "Image": img_64, "Shape": shape_string}
		payload = {"NodeID": "demo_entry", "Timestamp": time.time(), "Image": [img_64], "Shape": shape_string}

		headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
		result = requests.post(url, json=payload, headers=headers)
		print(result.json())
