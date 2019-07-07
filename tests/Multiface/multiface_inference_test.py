import configparser, logging, base64, time, json, requests, time
from PIL import Image
import numpy as np


## DO NOT change variables in this file. Go to config.ini

try: 
    config = configparser.ConfigParser()
    config.read('config.ini')
except:
    raise Exception("config.ini file not found.")

class MultifaceInferenceTest():
    def __init__(self, ):
        ## Logger
        level = self.log_level(config.get('DEFAULT', 'LogLevel'))
        self.logger = logging.getLogger(config.get('DEFAULT', 'Name'))
        self.logger.setLevel(level)
        ch = logging.FileHandler('multiface_inference_test_result.log')
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        ## Photo
        self.photo = self.load_photo(config.get('DEFAULT', 'PhotoName'))

        ## Loops
        self.loops = config.get('DEFAULT', 'Loops')

    def log_level(self, level):
        ## if level doesn't match any, return DEBUG
        if level == 'INFO':
            return logging.INFO
        elif level == 'DEBUG':
            return logging.DEBUG
        elif level == 'WARNING':
            return logging.WARNING
        elif level == 'ERROR':
            return logging.ERROR
        elif level == 'CRITICAL':
            return logging.CRITICAL
        else:
            return logging.DEBUG
    
    def load_photo(self, path):
        image = np.asarray(Image.open(path), dtype=np.uint8)
        shape_string = str(image.shape)
        image = image.astype(np.float64)
        img_64 = base64.b64encode(image).decode('ascii')
        return img_64

    def average_performance_test(self, img_64, shape_string, url):
        payload = {"NodeID": "demo_entry", "Timestamp": time.time(), "Image": img_64, "Shape": shape_string}
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        total_time = 0
        for i in range(self.loops):
            start = time.time()
            result = requests.post(url, json=payload, headers=headers)
            tof = time.time() - start 
            self.logger.warning("Request" + str(i) + " takes" + str(tof)
                )
            total_time+=tof
        self.logger.debug("Average request time:" + str(total_time/float(self.loops)))
        return result

    def execute_test(self,):
        #TODO
        return

if __name__ == '__main__':
    test = MultifaceInferenceTest()
    test.execute_test()

