import pymongo

class MongoClient():

    def __init__(self, db_name, port='mongodb://172.29.135.101:27017/'):
        self.client = pymongo.MongoClient(port)
        self.db = self.client[db_name]
        print(db_name, "Database created")
        self.face_collection = self.db['FaceCollection']
        print("FaceCollection initialized")

    def add_staff(self, adict):
        result = self.face_collection.insert_one(adict)
        return result.inserted_id

    def get_embedding_by_name(self, name):
        query = {'Name' : name}
        result = self.face_collection.find_one(query)['Embedding']
        return result

    def remove_staff(self, name):
        query = {'Name' : name}
        result = self.face_collection.delete_one(query)
        return result

    def find_all(self,):
        return self.face_collection.find()

    def delete_all(self):
        self.face_collection.delete_many({})

# if __name__ == '__main__':
#     client = MongoClient('hospital')
    # result = client.add_staff({'Name': "luka", "Embedding": "wadafuq"})
    # result = client.add_staff({'Name': "luka3", "Embedding": "wadafuq"})
    # result = client.add_staff({'Name': "luka4", "Embedding": "wadafuq"})
    # result = client.get_embedding_by_name('luka')
    # result = client.remove_staff('luka')
    # client.delete_all()
    # result = client.find_all()
    # for x in result:
    #     print(x)