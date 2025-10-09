#!/usr/bin/env python3
"""
Startup script for Healthify backend with MongoDB.
This script sets up MongoDB and starts the FastAPI server.
"""

import asyncio
import subprocess
import sys
import os
import time
import logging
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.config import settings
from setup_mongodb import setup_mongodb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_mongodb_connection():
    """Check if MongoDB is running and accessible."""
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        client = AsyncIOMotorClient(settings.mongo_url)
        await client.admin.command('ping')
        logger.info("MongoDB connection successful")
        return True
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        return False


async def setup_database():
    """Set up MongoDB database and collections."""
    try:
        logger.info("Setting up MongoDB database...")
        await setup_mongodb()
        logger.info("MongoDB setup completed")
        return True
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        return False


def start_server():
    """Start the FastAPI server."""
    try:
        logger.info("Starting FastAPI server...")
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=settings.debug,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


async def main():
    """Main startup function."""
    logger.info("Starting Healthify Backend with MongoDB")
    
    # Check MongoDB connection
    if not await check_mongodb_connection():
        logger.error("MongoDB is not accessible. Please ensure MongoDB is running.")
        logger.info("To start MongoDB locally:")
        logger.info("  - Windows: mongod --dbpath C:\\data\\db")
        logger.info("  - macOS: brew services start mongodb-community")
        logger.info("  - Linux: sudo systemctl start mongod")
        sys.exit(1)
    
    # Set up database
    if not await setup_database():
        logger.error("Database setup failed")
        sys.exit(1)
    
    # Start server
    logger.info("Starting FastAPI server...")
    start_server()


if __name__ == "__main__":
    asyncio.run(main())
