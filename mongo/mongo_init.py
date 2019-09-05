import unittest
import pymongo,datetime

class TestMongoDB(unittest.TestCase):

    def setUp(self, ):
        ## Move these variables to a config      
        self.db_name = 'Hospital'
        self.emb_collection_name = 'EmbeddingCollection'
        self.hygiene_collection_name = 'HygieneCollection'
        self.port = 'mongodb://localhost:27017/'
        self.client = pymongo.MongoClient(self.port)
        self.db = self.client[self.db_name]
        ## Personnel Information
        self.emb_collection = self.db[self.emb_collection_name]
        ## Hygiene Record
        self.hygiene_collection = self.db[self.hygiene_collection_name]
        ## Entry Units
        self.entry_collection = self.db['EntryUnit']
        ## Sanitizer Units
        self.sanitizer_collection = self.db['SanitizerUnit']

    def test_connection(self,):
        self.assertEqual(self.db.command("serverStatus")["connections"]['active'], 1)

    @unittest.expectedFailure
    def test_embedding_duplication(self, ):
        result = self.emb_collection.create_index('StaffID', unique=True)
        self.assertEqual(result, 'StaffID')

    @unittest.expectedFailure
    def test_entry_duplication(self, ):
        result = self.entry_collection.create_index('NodeID', unique=True)
        self.assertEqual(result, 'NodeID')

    @unittest.expectedFailure
    def test_sanitizer_duplication(self, ):
        result = self.sanitizer_collection.create_index('NodeID', unique=True)
        self.assertEqual(result, 'NodeID')

    @unittest.expectedFailure
    def test_expiration(self, ):
        self.assertRaises(pymongo.errors.OperationFailure, 
            self.hygiene_collection.create_index('Timestamp', expireAfterSeconds=30))

if __name__ == '__main__':
    unittest.main()
    ## TODO please define all the entry units and sanitizer units and their neighbours. 