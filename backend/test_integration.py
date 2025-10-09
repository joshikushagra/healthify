#!/usr/bin/env python3
"""
Integration test script for Healthify backend with MongoDB and MCP chatbot.
This script tests the basic functionality of the migrated system.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.database import get_async_mongo, get_async_mongo_collection
from app.services.mcp_chatbot import mcp_chatbot
from app.services.cache_service import cache_service
from app.config import settings


async def test_mongodb_connection():
    """Test MongoDB connection."""
    print("🔍 Testing MongoDB connection...")
    try:
        db = get_async_mongo()
        await db.command("ping")
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False


async def test_mongodb_collections():
    """Test MongoDB collections."""
    print("🔍 Testing MongoDB collections...")
    try:
        db = get_async_mongo()
        collections = await db.list_collection_names()
        print(f"✅ Found {len(collections)} collections: {collections}")
        return True
    except Exception as e:
        print(f"❌ MongoDB collections test failed: {e}")
        return False


async def test_cache_service():
    """Test cache service with MongoDB."""
    print("🔍 Testing cache service...")
    try:
        # Test cache operations
        test_key = "test_key"
        test_value = {"message": "Hello, World!", "timestamp": "2024-01-01"}
        
        # Set cache
        await cache_service.set(test_key, test_value, ttl=60)
        print("✅ Cache set operation successful")
        
        # Get cache
        cached_value = await cache_service.get(test_key)
        if cached_value == test_value:
            print("✅ Cache get operation successful")
        else:
            print("❌ Cache get operation failed - values don't match")
            return False
        
        # Delete cache
        await cache_service.delete(test_key)
        print("✅ Cache delete operation successful")
        
        return True
    except Exception as e:
        print(f"❌ Cache service test failed: {e}")
        return False


async def test_mcp_chatbot():
    """Test MCP chatbot service."""
    print("🔍 Testing MCP chatbot service...")
    try:
        # Test chat message processing
        test_message = "I have a headache and feel dizzy"
        user_id = "test_user_123"
        
        response = await mcp_chatbot.process_chat_message(
            message=test_message,
            user_id=user_id
        )
        
        print(f"✅ MCP chatbot response: {response.message[:100]}...")
        print(f"   - Is Medical: {response.is_medical}")
        print(f"   - Confidence: {response.confidence}")
        
        return True
    except Exception as e:
        print(f"❌ MCP chatbot test failed: {e}")
        return False


async def test_symptom_analysis():
    """Test symptom analysis."""
    print("🔍 Testing symptom analysis...")
    try:
        symptoms_data = {
            "symptoms": ["headache", "dizziness", "nausea"],
            "age": 30,
            "gender": "male",
            "medical_history": [],
            "current_medications": []
        }
        
        analysis = await mcp_chatbot.analyze_symptoms(symptoms_data, "test_user_123")
        
        print(f"✅ Symptom analysis completed")
        print(f"   - Conditions found: {len(analysis.conditions)}")
        print(f"   - Urgency: {analysis.triage_advice.urgency}")
        print(f"   - Confidence: {analysis.confidence_score}")
        
        return True
    except Exception as e:
        print(f"❌ Symptom analysis test failed: {e}")
        return False


async def test_database_operations():
    """Test basic database operations."""
    print("🔍 Testing database operations...")
    try:
        # Test chat sessions collection
        chat_collection = get_async_mongo_collection("chat_sessions")
        
        # Insert test document
        test_doc = {
            "user_id": "test_user_123",
            "session_id": "test_session_123",
            "is_active": True,
            "created_at": "2024-01-01T00:00:00Z",
            "messages": []
        }
        
        result = await chat_collection.insert_one(test_doc)
        print(f"✅ Document inserted with ID: {result.inserted_id}")
        
        # Find test document
        found_doc = await chat_collection.find_one({"session_id": "test_session_123"})
        if found_doc:
            print("✅ Document found successfully")
        else:
            print("❌ Document not found")
            return False
        
        # Clean up test document
        await chat_collection.delete_one({"session_id": "test_session_123"})
        print("✅ Test document cleaned up")
        
        return True
    except Exception as e:
        print(f"❌ Database operations test failed: {e}")
        return False


async def main():
    """Run all integration tests."""
    print("🚀 Starting Healthify Integration Tests")
    print("=" * 50)
    
    tests = [
        ("MongoDB Connection", test_mongodb_connection),
        ("MongoDB Collections", test_mongodb_collections),
        ("Cache Service", test_cache_service),
        ("Database Operations", test_database_operations),
        ("MCP Chatbot", test_mcp_chatbot),
        ("Symptom Analysis", test_symptom_analysis),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            if await test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
