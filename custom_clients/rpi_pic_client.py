from __future__ import print_function
import sys, os, requests, time, json, picamera, io
import RPi.GPIO as GPIO
from PIL import Image
from config import config
import base64


class PiClient:
    """
    Client class running on raspberry pi
    Two types: 
        -sanitizer client:
            takes picture when motion detector is triggered.
            posts request with image.
            waits for response from server, if fail, post again.
        -entry client:
            takes picture when motion detector is triggered.
            posts request with image.
            waits for response from server, if fail, post again;
                                            if breach, trigger alarm;
                                            if clean, continue.
    """
    def __init__(self):
        # TODO: set location in environment variable
        # get location/deviceID from envvar and init with client type
        self.ctype = os.environ['CLIENT_TYPE']
        self.node_id = os.environ['LOCATION']

        # camera init
        self.camera = picamera.PiCamera()
        self.camera.start_preview()
        time.sleep(2)

        # image place holder
        self.image = None

        # gpio pins initialization
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.IN)
        GPIO.setup(3, GPIO.OUT)


        if self.ctype == 'san':
            # sanitizer url?
            self.url = 'http:' + config.SERVER_HOST + ':' + config.SERVER_PORT + '/sanushost/api/v1.0/sanitizer_img'

        if self.ctype == 'ent':
            # entry url?
            self.url = 'http:' + config.SERVER_HOST + ':' + config.SERVER_PORT + '/sanushost/api/v1.0/entry_img'
        
    def capture_and_post(self):
        """
        Capture an image, and post request with b64 string
        return success if server return success/breach
        """
        timestamp = time.time()
        # TODO: add shape/resolution string from rpi camera
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        image_64 = str(base64.b64encode(open(stream, 'rb').read()).decode('ascii'))
        # timestamp here seconds since epoch, float
        payload = {'NodeID': self.node_id, 'Timestamp': timestamp, 'Image': image_64, 'Shape': shape}
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        result = None
        while result != 'Success':
            result = requests.post(self.url, json=payload, headers=headers)['Status']

        if self.ctype == 'ent' and result['Breach']:
            self.alert()
        return 1

    def alert(self):
        """
        Trigger breach alarm
        LED for now
        """
        GPIO.output(3, 1)
        # trigger led for 5 seconds
        time.sleep(5)
        return 1

    def sanitizer_proximity_loop(self):
        while True:
            i = GPIO.input(11)
            if i == 1:
                capped = capture_and_post()
                if capped:
                    time.sleep(30)

    def entry_proximity_loop(self):
        while True:
            i = GPIO.input(11)
            if i == 1:
                capped = capture_and_post()
                if capped:
                    time.sleep(30)


if __name__ == '__main__':
    client = PiClient()
    if client.ctype == 'san':
        client.sanitizer_proximity_loop()
    else:
        client.entry_proximity_loop()