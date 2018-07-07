import requests
import numpy as np
import dlib
import base64

url = 'http://localhost:5000/sanushost/api/v1.0/sanitizer_img'
image = dlib.load_rgb_image('/home/billy/Downloads/wjx_test_far_extreme.jpg')
print(image.shape)
image = image.astype(np.float64)
img_64 = base64.b64encode(image)
payload = {'Timestamp': 100, 'Location': '1', 'Image': img_64}
headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
result = requests.post(url, json=payload, headers=headers)
print(result.json())