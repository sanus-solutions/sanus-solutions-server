import datetime, pymongo, time

db_name = 'Hospital'
emb_collection_name = 'EmbeddingCollection'
hygiene_collection_name = 'HygieneCollection'
port = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(port)
db = client[db_name]
emb_collection = db[emb_collection_name]
hygiene_collection = db[hygiene_collection_name]

# result = emb_collection.insert_one({'Staff': "luka", 'Embedding': "Test"})
# result = emb_collection.insert_one({'Staff': "luka", 'Embedding': "Test"})

result = hygiene_collection.insert_one({'Staff': "luka", 'Timestamp': datetime.datetime.fromtimestamp(time.time()).replace(tzinfo=datetime.timezone.utc)})
print(result.acknowledged, result.inserted_id)
# time.sleep(35)
# for x in hygiene_collection.find():
# 	print(x)