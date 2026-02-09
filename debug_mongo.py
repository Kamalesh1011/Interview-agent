import logging
logging.basicConfig()
logging.getLogger('pymongo').setLevel(logging.DEBUG)
from pymongo import MongoClient
client = MongoClient("mongodb+srv://i103:aishu@cluster0.zxk94yv.mongodb.net/?appName=Cluster0", serverSelectionTimeoutMS=5000)
try:
    print(client.server_info())
except Exception as e:
    print(repr(e))