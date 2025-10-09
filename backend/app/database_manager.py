from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING, TEXT
from app.config import settings
import structlog
from typing import List
from app.utils.error_handlers import exception_handler, APIException
from app.api import health
from fastapi import FastAPI
from app.database_manager import db_manager

logger = structlog.get_logger()

class DatabaseManager:
    def __init__(self):
        self.async_client = None
        self.sync_client = None
        self._setup_clients()
        
    def _setup_clients(self):
        """Setup MongoDB clients with connection pooling."""
        # Async client with connection pooling
        self.async_client = AsyncIOMotorClient(
            settings.mongo_url,
            maxPoolSize=50,
            minPoolSize=10,
            maxIdleTimeMS=30000
        )
        
        # Sync client with connection pooling
        self.sync_client = MongoClient(
            settings.mongo_url,
            maxPoolSize=50,
            minPoolSize=10,
            maxIdleTimeMS=30000
        )
        
    async def setup_indexes(self):
        """Setup MongoDB indexes for better query performance."""
        db = self.async_client[settings.mongo_database]
        
        # User indexes
        await db.users.create_indexes([
            IndexModel([("email", ASCENDING)], unique=True),
            IndexModel([("username", ASCENDING)], unique=True),
            IndexModel([("created_at", DESCENDING)])
        ])
        
        # Patient indexes
        await db.patients.create_indexes([
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("email", ASCENDING)]),
            IndexModel([("name", TEXT)]),
            IndexModel([("created_at", DESCENDING)])
        ])
        
        # Chat indexes
        await db.chat_sessions.create_indexes([
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)])
        ])
        
        # Content indexes
        await db.content.create_indexes([
            IndexModel([("title", TEXT)]),
            IndexModel([("tags", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)])
        ])
        
        logger.info("Database indexes created successfully")
    
    async def health_check(self) -> bool:
        """Check database connection health."""
        try:
            await self.async_client[settings.mongo_database].command("ping")
            return True
        except Exception as e:
            logger.error("Database health check failed", error=str(e))
            return False
    
    def get_async_db(self):
        """Get async database instance."""
        return self.async_client[settings.mongo_database]
    
    def get_sync_db(self):
        """Get sync database instance."""
        return self.sync_client[settings.mongo_database]
    
    async def close(self):
        """Close database connections."""
        if self.async_client:
            self.async_client.close()
        if self.sync_client:
            self.sync_client.close()

# Create global instance
db_manager = DatabaseManager()
# Initialize FastAPI app
app = FastAPI()

app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(Exception, exception_handler)
app.include_router(health.router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    await db_manager.setup_indexes()

@app.on_event("shutdown")
async def shutdown():
    await db_manager.close()