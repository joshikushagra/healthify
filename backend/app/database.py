from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# MongoDB setup
mongo_client = MongoClient(settings.mongo_url)
async_mongo_client = AsyncIOMotorClient(settings.mongo_url)

def get_mongo():
    """Get synchronous MongoDB database instance."""
    return mongo_client[settings.mongo_database]

def get_async_mongo():
    """Get asynchronous MongoDB database instance."""
    return async_mongo_client[settings.mongo_database]

def get_mongo_collection(collection_name: str):
    """Get a specific MongoDB collection."""
    return get_mongo()[collection_name]

def get_async_mongo_collection(collection_name: str):
    """Get a specific async MongoDB collection."""
    return get_async_mongo()[collection_name]
