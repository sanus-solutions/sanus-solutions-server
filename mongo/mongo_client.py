import pymongo, logging, configparser, json
from bson import json_util

try: 
    config = configparser.ConfigParser()
    config.read('mongo_config.ini')
except:
    raise Exception("mongo_config.ini file not found.")

class MongoClient():

    def __init__(self, 
        db_name=config.get('MONGO', 'Database'),
        collection_name=config.get('MONGO', 'FaceCollection'), 
        port=config.get('MONGO', 'URL')):
        ## Logger
        level = self.log_level(config.get('DEFAULT', 'LogLevel'))
        self.logger = logging.getLogger(config.get('DEFAULT', 'Name'))
        self.logger.setLevel(level)
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
        self.face_collection = self.db[collection_name]

        ## TODO 
        ## If DB has duplicated keys exit when unique ID is true, raise duplicate key errors
        if config.getboolean('MONGO', 'UniqueID'):
            ## Need to read more docs on collection index
            self.face_collection.create_index('user_id', unique=1)
        else:
            self.face_collection.drop_indexes()

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

    def add_staff(self, adict):
        ## Implement a format check here in the future
        try:
            result = self.face_collection.insert_one(adict)
            self.logger.debug("Staff insertion accepted, job_id: %s", result.inserted_id)
            return result
        except pymongo.errors.DuplicateKeyError:
            self.logger.debug("Staff alredy exits. Removing old record and reinsert")

            ## Temporary solutions - replace_one raise errors because unique id is immutable.
            ## Implement update_one in the future when the dictionary keys are certain
            self.remove_staff(adict['Name'])
            result = self.face_collection.insert_one(adict)

            self.logger.debug("Staff insertion accepted, job_id: %s", result.inserted_id)
            return result
        except:
            ## TODO
            self.logger.debug("[Critical] Other uncaught errors.")
        
    def get_embedding_by_name(self, name):
        query = {'Name' : name}
        result = self.face_collection.find_one(query)['Embedding']
        return result

    def remove_staff(self, name):
        ## Implement a format check here in the future
        try:
            query = {'Name' : name}
            result = self.face_collection.delete_one(query)
            self.logger.debug("Staff deletion %s", result.raw_result)
            return result
        except:
            ## TODO 
            self.logger.debug("[Critical] Other uncaught errors.")

    def find_all(self,):
        return self.face_collection.find()

    def delete_all(self):
        self.face_collection.delete_many({})

if __name__ == '__main__':
    client = MongoClient('hospital')
    result = client.add_staff({'Name': "luka", "Embedding": "wadafuq"})
    # print(result, type(result), type(result.inserted_id))
    # result = client.add_staff({'Name': "luka", "Embedding": "wadafuq"})
    # result = client.add_staff({'Name': "luka3", "Embedding": "wadafuq"})
    # result = client.add_staff({'Name': "luka4", "Embedding": "wadafuq"})
    # result = client.get_embedding_by_name('luka')
    # result = client.remove_staff('luka')
    # client.delete_all()
    result = client.find_all()
    for x in result:
        print(x)