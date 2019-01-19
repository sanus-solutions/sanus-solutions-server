from flask import Flask, request, json
import numpy as np
import json, base64, ast, cv2, time, logging, os
## Clients 
from util import Rekognition

app = Flask(__name__)

if os.path.isfile('config.ini') and os.path.isfile('credentials.csv'):
    rek = Rekognition.Rekognition('credentials.csv', 'config.ini')
else:
    raise Exception("Credentials or config.ini missing.")

logger = logging.getLogger('Rekognition Docker log')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

"""
route for aws facial rekognition
request payload format:
{'Image': Bytes, 'Collection': string}
Responses: 
{"Image":img_64, 'Shape': shape_string}
"""
@app.route('/rekognition', methods=['POST'])
def rekognition():
    logger.debug("Object received")
    json_data = request.get_json()
    image_bytes = json_data['Image']
    collection_id = json_data['Collection']
    candidate = rek.search_face_in_collection(collection_id, image_bytes)
    if candidate:
        ## literal may not ba able to cast to string 
        return json.dumps({'Status': str(candidate)})
    else:
        return json.dumps({'Status': 'no face'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
    logger.info("Initialize rekognition container.")