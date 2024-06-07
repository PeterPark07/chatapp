from pymongo import MongoClient
import os

# Connect to MongoDB
mongo_client = MongoClient(os.getenv('mongodb'))
database = mongo_client['chat']
collection = os.getenv('collection')
messages_collection = database[collection]