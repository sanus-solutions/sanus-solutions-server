import requests
import numpy as np
import dlib
import base64
import ast
import scipy.misc
import time

url = 'http://localhost:5000/sanushost/api/v1.0/entry_img'
# url = 'http://localhost:5000/sanushost/api/v1.0/sanitizer_img'
# image = dlib.load_rgb_image('/home/billyzheng/Downloads/klaus2.jpg')

image = dlib.load_rgb_image('/home/billyzheng/Downloads/klausz.jpeg')
image = scipy.misc.imresize(image, 0.8)

shape_string = str(image.shape)
image = image.astype(np.float64)
# image_temp = np.reshape(image, (1, image.shape[0]*image.shape[1]*image.shape[2]))
img_64 = base64.b64encode(image).decode('ascii')
# payload = {"NodeID": "demo_sanitizer", "Timestamp": [time.time()], "Image": img_64, "Shape": shape_string}
payload = {"NodeID": "demo_entry", "Timestamp": [time.time()], "Image": img_64, "Shape": shape_string}
headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
result = requests.post(url, json=payload, headers=headers)
print(result.json())