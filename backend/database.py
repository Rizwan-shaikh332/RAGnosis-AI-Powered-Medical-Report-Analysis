from pymongo import MongoClient
from config import Config

_client = None

def get_db():
    global _client
    if _client is None:
        _client = MongoClient(Config.MONGODB_URI)
    return _client[Config.DB_NAME]
