import json
from typing import Any, Optional
from app.database import get_async_mongo
from app.config import settings
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self):
        self.default_ttl = 3600  # 1 hour
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            db = get_async_mongo()
            doc = await db.cache.find_one({"_id": key})
            if doc and (not doc.get("expires_at") or doc["expires_at"] > datetime.utcnow()):
                return doc["value"]
            return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {str(e)}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache."""
        try:
            db = get_async_mongo()
            ttl = ttl or self.default_ttl
            expires_at = datetime.utcnow() + timedelta(seconds=ttl)
            await db.cache.update_one(
                {"_id": key},
                {"$set": {"value": value, "expires_at": expires_at}},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            db = get_async_mongo()
            await db.cache.delete_one({"_id": key})
            return True
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {str(e)}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            db = get_async_mongo()
            doc = await db.cache.find_one({"_id": key})
            return doc is not None
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {str(e)}")
            return False
    
    async def get_or_set(self, key: str, func, ttl: Optional[int] = None, *args, **kwargs) -> Any:
        """Get value from cache or set it using provided function."""
        cached_value = await self.get(key)
        if cached_value is not None:
            return cached_value
        
        # Generate new value
        new_value = await func(*args, **kwargs) if callable(func) else func
        
        # Cache the new value
        await self.set(key, new_value, ttl)
        return new_value
    
    def generate_key(self, prefix: str, *args) -> str:
        """Generate a cache key from prefix and arguments."""
        key_parts = [prefix] + [str(arg) for arg in args]
        return ":".join(key_parts)


# Global cache service instance
cache_service = CacheService()
