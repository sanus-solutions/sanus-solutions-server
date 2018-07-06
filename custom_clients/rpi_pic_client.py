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
        self.device_id = os.environ['LOCATION']

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
        
    def capture(self):
        """
        Capture an image, and post request with b64 string
        """
        timestamp = time.time()
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        image_64 = str(base64.b64encode(open(stream, 'rb').read()).decode('ascii'))
        # timestamp here seconds since epoch, float
        payload = {'Timestamp': timestamp, 'Location': self.device_id, 'Image': image_64}
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        result = requests.post(self.url, json=payload, headers=headers)

        if self.ctype 
        

    def alert(self):
        """
        Trigger breach alarm
        LED for now
        """
        GPIO.output(3, 1)
        # trigger led for 5 seconds
        time.sleep(5)
        return 1

