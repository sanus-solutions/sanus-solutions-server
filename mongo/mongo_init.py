import unittest
import pymongo,datetime



# result = emb_collection.insert_one({'Staff': "luka", 'Embedding': "Test"})
# result = hygiene_collection.insert_one({'Staff': "luka", 'Timestamp': datetime.datetime.utcnow()})

class TestMongoDB(unittest.TestCase):

    def setUp(self, ):
        ## Move these variables to a config      
        self.db_name = 'Hospital'
        self.emb_collection_name = 'EmbeddingCollection'
        self.hygiene_collection_name = 'HygieneRecord'
        self.port = 'mongodb://localhost:27017/'
        self.client = pymongo.MongoClient(self.port)
        self.db = self.client[self.db_name]
        self.emb_collection = self.db[self.emb_collection_name]
        self.hygiene_collection = self.db[self.hygiene_collection_name]

    def test_connection(self,):
        self.assertEqual(self.db.command("serverStatus")["connections"]['active'], 1)

    ##TODO 
    @unittest.expectedFailure
    def test_duplication(self, ):
        result = self.emb_collection.create_index('Staff', unique=True)
        self.assertEqual(result, 'Staff')

    ##TODO
    @unittest.expectedFailure
    def test_expiration(self, ):
        self.assertRaises(pymongo.errors.OperationFailure, 
            self.hygiene_collection.create_index('Timestamp', expireAfterSeconds=30))

if __name__ == '__main__':
    unittest.main()