"""
Database viewer script for Healthify
Run this script to view the contents of your MongoDB collections
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from bson import json_util
import json
from datetime import datetime
import os

# MongoDB connection settings
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "healthify"

async def view_collections():
    """View all collections and their contents"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Get all collection names
    collections = await db.list_collection_names()
    
    print(f"\n{'='*50}")
    print(f"Database: {DB_NAME}")
    print(f"{'='*50}")
    
    for collection_name in collections:
        print(f"\n{'-'*20} {collection_name} {'-'*20}")
        
        # Get collection stats
        stats = await db.command("collStats", collection_name)
        doc_count = stats["count"]
        size = stats["size"] / 1024  # Convert to KB
        
        print(f"Documents: {doc_count}")
        print(f"Size: {size:.2f} KB")
        
        # Get sample documents
        cursor = db[collection_name].find().limit(3)
        documents = await cursor.to_list(length=3)
        
        if documents:
            print("\nSample documents:")
            for doc in documents:
                # Convert ObjectId to string for better readability
                doc_str = json.loads(json_util.dumps(doc))
                print(json.dumps(doc_str, indent=2))
        
        print(f"{'='*50}")

async def view_collection_details(collection_name):
    """View detailed information about a specific collection"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    if collection_name not in await db.list_collection_names():
        print(f"Collection '{collection_name}' not found!")
        return
    
    print(f"\n{'='*50}")
    print(f"Collection: {collection_name}")
    print(f"{'='*50}")
    
    # Get collection stats
    stats = await db.command("collStats", collection_name)
    
    print("\nCollection Statistics:")
    print(f"Document Count: {stats['count']}")
    print(f"Size: {stats['size']/1024:.2f} KB")
    print(f"Average Document Size: {stats['avgObjSize']/1024:.2f} KB" if stats['count'] > 0 else "Average Document Size: N/A")
    
    # Get indexes
    indexes = await db[collection_name].index_information()
    print("\nIndexes:")
    for name, info in indexes.items():
        print(f"- {name}: {info['key']}")
    
    # Show sample documents
    print("\nSample Documents:")
    cursor = db[collection_name].find().limit(5)
    documents = await cursor.to_list(length=5)
    
    for doc in documents:
        doc_str = json.loads(json_util.dumps(doc))
        print(json.dumps(doc_str, indent=2))

def main():
    """Main function to run the database viewer"""
    while True:
        print("\nHealthify Database Viewer")
        print("1. View all collections")
        print("2. View specific collection")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            asyncio.run(view_collections())
        elif choice == "2":
            collection_name = input("Enter collection name: ")
            asyncio.run(view_collection_details(collection_name))
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()