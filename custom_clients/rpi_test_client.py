import sys, os, requests, time, json, picamera, io, base64
from PIL import Image

class PiClient:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.start_preview()
        time.sleep(2)
        self.url = 'http://192.168.1.169:5000/sanushost/api/v1.0/sanitizer_img'
        self.node_id = '1'
        self.shape = '(1920, 1080)'
    def capture_and_post(self):
        timestamp = time.time()
        stream = io.BytesIO()
        self.camera.capture(stream, format='jpeg')
        stream.seek(0)

        image_64 = str(base64.b64encode(open(stream, 'rb').read()).decode('ascii'))
        payload = {'NodeID': self.node_id, 'Timestamp': timestamp, 'Image': image_64, 'Shape': self.shape}
        headers = {'Content_Type': 'application/json', 'Accept': 'text/plain'}
        result = requests.post(self.url, json=payload, headers=headers)

        print(result)
        return result



if __name__ == '__main__':
    client = PiClient()
    countdown = 5
    while countdown >= 0:
        print(countdown)
        sleep(0.8)
        countdown = countdown - 1
        if countdown == 0:
            print 'Taking pic'
            break
    client.capture_and_post()