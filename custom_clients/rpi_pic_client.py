from __future__ import print_function
import sys, os, requests, time, json, picamera
import RPi.GPIO as GPIO


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
    def __init__(self, client_type):
        # init with client type
        self.ctype = client_type

        # camera init
        self.camera = picamera.PiCamera()

        # image place holder
        self.image = None

        # gpio pins initialization
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.IN)
        GPIO.setup(3, GPIO.OUT)


        if self.ctype == 'san':
            # sanitizer url?
            self.url = 'sanushost/sanitizer'

        if self.ctype == 'ent':
            # entry url?
            self.url = 'sanushost/entry'

    def post(self):
        """
        Post request with image
        """
        


    def alert(self):
        """
        Trigger breach alarm
        LED for now
        """
        GPIO.output(3, 1)
        # trigger led for 5 seconds
        time.sleep(5)
        return 1

