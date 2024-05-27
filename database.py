from pymongo import MongoClient
import os

# Connect to MongoDB
mongo_client = MongoClient(os.getenv('mongodb'))
database = mongo_client['chat']
messages_collection = database['message_log']
