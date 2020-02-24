import requests
import numpy as np
import base64
import time
import json 
import cv2


#########################################################################################################
# Edit variables here
#########################################################################################################

file_path = 'teacherFacesV1/teacherB.jpg'
name_appeared_in_database = 'teacher'

url = 'http://localhost:5000/sanushost/api/v1.0/add_face'
#########################################################################################################
# Try not to touch this section
#########################################################################################################

image = cv2.imread(file_path)
shape_string = str(image.shape)
# print(shape_string)
retval, buffer = cv2.imencode('.jpg', image)
jpg_as_text = base64.b64encode(buffer)
payload = {"Staff": "childI", "Image": jpg_as_text, "Shape": shape_string}
headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
result = requests.post(url, json=payload, headers=headers)
json_data = result.json()
print(json_data)
