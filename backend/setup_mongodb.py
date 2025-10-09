#!/usr/bin/env python3
"""
MongoDB setup script for Healthify backend.
This script creates the necessary collections and indexes for the application.
"""

import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def setup_mongodb():
    """Set up MongoDB collections and indexes."""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(settings.mongo_url)
        db = client[settings.mongo_database]
        
        # Test connection
        await client.admin.command('ping')
        logger.info("Connected to MongoDB successfully")
        
        # Create collections with indexes
        collections_config = {
            "users": [
                ("email", 1),  # Unique index on email
                ("username", 1),  # Unique index on username
            ],
            "chat_sessions": [
                ("user_id", 1),
                ("session_id", 1),
                ("created_at", -1),
            ],
            "symptom_analyses": [
                ("user_id", 1),
                ("created_at", -1),
            ],
            "cache": [
                ("expires_at", 1),  # TTL index for cache expiration
            ],
            "audit_logs": [
                ("user_id", 1),
                ("action", 1),
                ("created_at", -1),
            ],
            "patients": [
                ("user_id", 1),
                ("patient_id", 1),
            ],
            "medical_records": [
                ("patient_id", 1),
                ("created_at", -1),
            ],
            "appointments": [
                ("patient_id", 1),
                ("doctor_id", 1),
                ("appointment_date", 1),
            ],
            "content": [
                ("category", 1),
                ("created_at", -1),
            ],
        }
        
        # Create collections and indexes
        for collection_name, indexes in collections_config.items():
            collection = db[collection_name]
            
            # Create collection if it doesn't exist
            if collection_name not in await db.list_collection_names():
                await collection.create_index("_id")
                logger.info(f"Created collection: {collection_name}")
            
            # Create indexes
            for index_spec in indexes:
                if len(index_spec) == 2:
                    field, direction = index_spec
                    try:
                        await collection.create_index([(field, direction)])
                        logger.info(f"Created index on {collection_name}.{field}")
                    except Exception as e:
                        logger.warning(f"Index creation failed for {collection_name}.{field}: {e}")
                elif len(index_spec) == 3:
                    field, direction, options = index_spec
                    try:
                        await collection.create_index([(field, direction)], **options)
                        logger.info(f"Created index on {collection_name}.{field} with options")
                    except Exception as e:
                        logger.warning(f"Index creation failed for {collection_name}.{field}: {e}")
        
        # Create TTL index for cache collection
        try:
            await db.cache.create_index("expires_at", expireAfterSeconds=0)
            logger.info("Created TTL index for cache collection")
        except Exception as e:
            logger.warning(f"TTL index creation failed: {e}")
        
        # Create compound indexes for better query performance
        compound_indexes = [
            ("chat_sessions", [("user_id", 1), ("is_active", 1)]),
            ("symptom_analyses", [("user_id", 1), ("status", 1)]),
            ("audit_logs", [("user_id", 1), ("action", 1), ("created_at", -1)]),
            ("appointments", [("patient_id", 1), ("appointment_date", 1)]),
        ]
        
        for collection_name, index_fields in compound_indexes:
            try:
                await db[collection_name].create_index(index_fields)
                logger.info(f"Created compound index for {collection_name}")
            except Exception as e:
                logger.warning(f"Compound index creation failed for {collection_name}: {e}")
        
        logger.info("MongoDB setup completed successfully")
        
    except Exception as e:
        logger.error(f"MongoDB setup failed: {str(e)}")
        raise
    finally:
        client.close()


async def main():
    """Main function to run the setup."""
    await setup_mongodb()


if __name__ == "__main__":
    asyncio.run(main())
