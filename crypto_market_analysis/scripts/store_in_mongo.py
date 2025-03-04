import pymongo
from pymongo import MongoClient
import json
from dotenv import load_dotenv
import os

load_dotenv()

def store_in_mongo():
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client['crypto_db']
    collection = db['crypto_data']

    with open('data/crypto_data.json') as f:
        data = json.load(f)

    result = collection.insert_many(data)
    print(f"Se insertaron {len(result.inserted_ids)} documentos en MongoDB")

store_in_mongo()
