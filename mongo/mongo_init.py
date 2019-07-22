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
        # hygiene_collection = db[hygiene_collection_name]
        # emb_collection.create_index('Staff', unique=True)
        # hygiene_collection.create_index('Timestamp', expireAfterSeconds=30)

    def test_connection(self,):
        self.assertEqual(self.db.command("serverStatus")["connections"]['active'], 1)
        
    def test__parse_url(self):
        self.assertEqual(('localhost', 27017), self.client.address)

    @unittest.expectedFailure
    def test_duplication(self, ):
        self.assertEqual(1, 1, "broken")

if __name__ == '__main__':
    unittest.main()