import requests
import numpy as np
import base64
import ast
import argparse
from PIL import Image

parser = argparse.ArgumentParser(description='Adding face to face collection')
parser.add_argument('image_fname', help='filename of image containing the face to be added')
parser.add_argument('face_id', help='id of added face')
args = parser.parse_args()

url = 'http://localhost:5000/sanushost/api/v1.0/add_face'
# TODO laad image here
image = np.asarray(Image.open(args.image_fname), dtype=np.uint8)
shape_string = str(image.shape)
image = image.astype(np.float64)
img_64 = base64.b64encode(image).decode('ascii')
payload = {"Image": img_64, "Shape": shape_string, "ID": args.face_id}
headers = {"Content-Type": "application/json", "Accept": "text/plain"}
result = requests.post(url, json=payload, headers=headers)
