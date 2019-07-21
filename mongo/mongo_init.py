import pymongo 

## Move these variables to a config
db_name = 'Hospital'
emb_collection_name = 'EmbeddingCollection'
hygiene_collection_name = 'HygieneRecord'
port = 'mongodb://localhost:27017/'

client = pymongo.MongoClient(port)
db = client[db_name]
emb_collection = db[emb_collection_name]
hygiene_collection = db[hygiene_collection_name]

emb_collection.create_index('Staff', unique=True)
result = emb_collection.insert_one({'Staff': "luka", 'Embedding': "Test"})
result = emb_collection.insert_one({'Staff': "luka", 'Embedding': "Test"})