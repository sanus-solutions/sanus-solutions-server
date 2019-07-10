import os, base64, requests
import numpy as np
from PIL import Image

url = 'http://172.29.135.101:5000/sanushost/api/v1.0/add_face'
headers = {"Content-Type": "application/json", "Accept": "text/plain"}

image = np.asarray(Image.open('trump.jpg'), dtype=np.uint8)
shape_string = str(image.shape)
image = image.astype(np.float64)
img_64 = base64.b64encode(image).decode('ascii')
payload = {"Image": img_64, "Shape": shape_string, "ID": 'trump'}
result = requests.post(url, json=payload, headers=headers)