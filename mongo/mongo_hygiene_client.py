import pymongo, logging, configparser
## Debug
import time

try: 
    config = configparser.ConfigParser()
    config.read('config/mongo_hygiene_config.ini')
except:
    raise Exception("mongo_hygiene_config.ini file not found.")

class MongoClient():

    def __init__(self, 
        db_name=config.get('MONGO', 'Database'),
        collection_name=config.get('MONGO', 'Collection'), 
        port=config.get('MONGO', 'URL')):
        ## Logger
        level = self.log_level(config.get('DEFAULT', 'LogLevel'))
        self.logger = logging.getLogger(config.get('DEFAULT', 'Name'))
        self.logger.setLevel(level)

        ## Temporary streamhandler for debug
        # ch = logging.FileHandler("MongoDB_hygiene.log")
        ch = logging.StreamHandler()

        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        ## Mongo DB client
        self.client = pymongo.MongoClient(port)
        try:
            self.logger.info(self.client.admin.command('ismaster'))
        except pymongo.errors.ConnectionFailure:
            self.logger.info('Server not available.')

        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

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

    def insert_record(self, new_dictionary):
        try:
            result = self.collection.insert_one(new_dictionary)
            self.logger.debug("Record insertion accepted, job_id: %s", result.inserted_id)
            return result
        except:
            ## TODO
            self.logger.debug("[Critical insertion error] Other uncaught errors.")
            return None

    def remove_record(self, id):
        try:
            query = {'_id' : id}
            result = self.collection.delete_one(query)
            self.logger.debug("Record deletion %s", result.raw_result)
            return result
        except:
            ## TODO 
            self.logger.debug("[Critical deletion error] Other uncaught errors.")
            return None

    def find(self, field, key):
        try:
            query = {field : key}
            result = self.collection.find(query)
            return result
        except: 
            None

    def find_all(self,):
        return self.collection.find()

    def delete_all(self):
        self.collection.delete_many({})

# if __name__ == '__main__':
    # client = MongoClient('hospital')
    # result = client.insert_record({'NodeID': 'Dispenser2', 'Timestamp': time.time(), 'Staff': 'luka'})
    # result = client.insert_record({'Node': 'Dispenser3', 'Time': time.time(), 'StaffName': 'luka'})
    # result = client.insert_record({'Node': 'Dispenser4', 'Time': time.time(), 'StaffName': 'luka1'})
    # result = client.insert_record({'Node': 'Dispenser5', 'Time': time.time(), 'StaffName': 'luka2'})
    # result = client.insert_record({'Node': 'Dispenser6', 'Time': time.time(), 'StaffName': 'luka1'})
    # result = client.insert_record({'Node': 'Dispenser7', 'Time': time.time(), 'StaffName': 'luka'})

    # print(result.raw_result['n'])
    # client.delete_all()
    # result = client.find_all()
    # result = client.find('StaffName', 'luka1').count()
    # print(result)
    # for x in result:
    #     print(x)