import pymongo

class MongoClient():

    def __init__(self, port='mongodb://localhost:27017/'):
        self.client = pymongo.MongoClient(port)
        return



    def check_connection(self, ):
        return

if __name__ == '__main__':
    client = MongoClient()
    print("success")