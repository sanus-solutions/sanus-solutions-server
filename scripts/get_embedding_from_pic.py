import requests
import numpy as np
import base64
import time
from PIL import Image

url = 'http://localhost:5000/sanushost/api/v1.0/entry_img'

## suppy pic file
image = np.array(Image.open('simeon.jpeg'))
shape_string = str(image.shape)
image_temp = image.astype(np.float64)
image_64 = base64.b64encode(image_temp).decode('ascii')
payload = {"NodeID": "demo_entry", "Timestamp": time.time(), "Image": image_64, "Shape": shape_string}
headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
result = requests.post(url, json=payload, headers=headers)
array = np.array(result.json()['embedding'][2:-2].split()).astype(np.float)
np.save('embedding0', np.expand_dims(array, axis=0))
