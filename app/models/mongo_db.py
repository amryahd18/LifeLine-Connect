"""
Project: LifeLine Connect (Blood Bank Network)
Component: MongoDB Client & Collection Access Layer
"""

from typing import Optional
import pymongo
from app.config import Config

_mongo_client: Optional[pymongo.MongoClient] = None

def get_mongo_client() -> pymongo.MongoClient:
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = pymongo.MongoClient(Config.MONGO_URI)
    return _mongo_client

def get_mongo_db():
    client = get_mongo_client()
    return client[Config.MONGO_DB]

def get_collection(name: str):
    db = get_mongo_db()
    return db[name]
