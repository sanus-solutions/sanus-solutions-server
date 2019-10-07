import pymongo, logging, configparser

try: 
    config = configparser.ConfigParser()
    config.read('config/mongo_face_config.ini')
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
        # ch = logging.FileHandler("MongoDB_face.log")
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

    def add_staff(self, new_dictionary):
        ## Implement a format check here in the future
        try:
            result = self.collection.insert_one(new_dictionary)
            self.logger.debug("Staff insertion accepted, job_id: %s", result.inserted_id)
            return result
        except pymongo.errors.DuplicateKeyError:

            ## Temporary solutions - replace_one raise errors because unique id is immutable.
            ## Implement update_one in the future when the dictionary keys are certain
            self.remove_staff(new_dictionary['Name'])
            result = self.collection.insert_one(new_dictionary)
            self.logger.debug("Staff already exits. Removed old record and reinsert, job_id: %s", result.inserted_id)
            return result
        except:
            ## TODO
            self.logger.debug("[Critical insertion error] Other uncaught errors.")
            return None
        
    def get_embedding_by_name(self, name):
        query = {'Name' : name}
        result = self.collection.find_one(query)['Embedding']
        return result

    def remove_staff(self, name):
        ## Implement a format check here in the future
        try:
            query = {'Name' : name}
            result = self.collection.delete_one(query)
            self.logger.debug("Staff deletion %s", result.raw_result)
            return result
        except:
            ## TODO 
            self.logger.debug("[Critical deletion error] Other uncaught errors.")
            return None

    def find_all(self,):
        return self.collection.find()

    def delete_all(self):
        self.collection.delete_many({})

if __name__ == '__main__':
    client = MongoClient('hospital')
    result = client.add_staff({'user_id': 1, 'Name': "luka", "Embedding": "wadafuq"})
    # print(result, type(result), type(result.inserted_id))
    # result = client.add_staff({'Name': "luka", "Embedding": "wadafuq"})
    # result = client.add_staff({'Name': "luka3", "Embedding": "wadafuq"})
    # result = client.get_embedding_by_name('luka')
    # result = client.remove_staff('luka')
    # print(result.raw_result['n'])
    # client.delete_all()
    # result = client.find_all()
    # for x in result:
    #     print(x)
