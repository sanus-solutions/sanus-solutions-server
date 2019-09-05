import requests
import numpy as np
import base64
import time
import json 
import cv2


# url = 'http://192.168.1.101:5000/sanushost/api/v1.0/identify_face'
# url = 'http://192.168.1.101:5000/sanushost/api/v1.0/update_staff_status_clean'
url = 'http://192.168.1.101:5000/sanushost/api/v1.0/check_staff_hygiene_status'
# image = dlib.load_rgb_image('/home/billyzheng/Downloads/klaus2.jpg')

image = cv2.imread('luka.png')
shape_string = str(image.shape)

retval, buffer = cv2.imencode('.jpg', image)
jpg_as_text = base64.b64encode(buffer)
payload = {"NodeID": "demo_sanitizer", "Timestamp": time.time(), "Image": jpg_as_text, "Shape": shape_string}

headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
result = requests.post(url, json=payload, headers=headers)