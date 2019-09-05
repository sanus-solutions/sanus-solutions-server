import requests
import numpy as np
from PIL import Image
import base64
import ast
import time
import json 


# url = 'http://192.168.1.101:5000/sanushost/api/v1.0/identify_face'
# url = 'http://192.168.1.101:5000/sanushost/api/v1.0/update_staff_status_clean'
url = 'http://192.168.1.101:5000/sanushost/api/v1.0/check_staff_hygiene_status'
# image = dlib.load_rgb_image('/home/billyzheng/Downloads/klaus2.jpg')

a = time.time()
image = np.asarray(Image.open('luka.png'), dtype=np.uint8)
# image = dlib.load_rgb_image('rupert.png')

shape_string = str(image.shape)
print(shape_string)
image = image.astype(np.float64)
# image_temp = np.reshape(image, (1, image.shape[0]*image.shape[1]*image.shape[2]))
img_64 = base64.b64encode(image).decode('ascii')
# payload = {"NodeID": "demo_sanitizer", "Timestamp": time.time(), "Image": img_64, "Shape": shape_string}
payload = {"Timestamp": time.time(), "StaffList": ['klaus', 'luka', 'steven']}

headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
result = requests.post(url, json=payload, headers=headers)
print(result.json())
print(time.time() - a)
