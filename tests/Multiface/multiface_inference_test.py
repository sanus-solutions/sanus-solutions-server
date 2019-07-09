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
        self.photo, self.size = self.load_photo(config.get('DEFAULT', 'PhotoName'))

        ## Loops
        self.loops = config.get('DEFAULT', 'Loops')

        ## url
        self.url = config.get('DEFAULT', 'URL')

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
        return img_64, shape_string

    def average_performance_test(self):
        payload = {"NodeID": "demo_entry", "Timestamp": time.time(), "Image": self.photo, "Shape": self.size}
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        time_list = []
        for i in range(int(self.loops)):
            start = time.time()
            result = requests.post(self.url, json=payload, headers=headers)
            tof = time.time() - start 
            self.logger.debug("Request" + str(i) + " takes " + str(tof)
                )
            time_list.append(tof)
        self.logger.debug("Average request time: " + str(np.average(time_list)))
        self.logger.debug("Standard deviation: " + str(np.std(time_list)))
        return result

    def execute_test(self,):
        
        return

if __name__ == '__main__':
    test = MultifaceInferenceTest()
    result = test.average_performance_test()
    

