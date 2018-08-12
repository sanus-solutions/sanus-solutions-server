import requests
import numpy as np
import dlib
import base64
import ast

url = 'http://localhost:5000/sanushost/api/v1.0/sanitizer_img'
image = dlib.load_rgb_image('/home/billy/Downloads/wjx_test_far_extreme.jpg')
shape_string = str(image.shape)
image = image.astype(np.float64)
<<<<<<< Updated upstream
img_64 = base64.b64encode(image)
=======
# image_temp = np.reshape(image, (1, image.shape[0]*image.shape[1]*image.shape[2]))
img_64 = base64.b64encode(image).decode('ascii')
>>>>>>> Stashed changes
payload = {'Timestamp': 100, 'NodeID': '1', 'Image': img_64, 'Shape': shape_string}
headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
result = requests.post(url, json=payload, headers=headers)
print(result.json())