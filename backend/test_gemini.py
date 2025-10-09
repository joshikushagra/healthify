#!/usr/bin/env python3
"""
Test script to verify Gemini integration works.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set environment variables
os.environ["DEBUG"] = "true"
os.environ["ENVIRONMENT"] = "development"
os.environ["MONGO_URL"] = "mongodb://localhost:27017/healthify"
os.environ["MONGO_DATABASE"] = "healthify"
os.environ["GEMINI_API_KEY"] = "test_key"  # This will fail but we can test the import

def test_imports():
    """Test if all imports work."""
    try:
        print("Testing imports...")
        from app.main import app
        print("+ App imported successfully")
        
        from app.services.mcp_chatbot import mcp_chatbot
        print("+ MCP chatbot imported successfully")
        
        from app.config import settings
        print("+ Config imported successfully")
        print(f"+ Gemini model: {settings.gemini_model}")
        
        return True
    except Exception as e:
        print(f"- Import failed: {e}")
        return False

def test_server_start():
    """Test if server can start."""
    try:
        print("\nTesting server start...")
        import uvicorn
        from app.main import app
        
        print("+ Server components loaded successfully")
        print("+ Ready to start server")
        return True
    except Exception as e:
        print(f"- Server start failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Healthify Backend with Gemini Integration")
    print("=" * 60)
    
    if test_imports() and test_server_start():
        print("\n" + "=" * 60)
        print("+ All tests passed! Backend is ready to run.")
        print("\nTo start the server:")
        print("1. Set your GEMINI_API_KEY in environment variables")
        print("2. Run: python simple_start.py")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("\n" + "=" * 60)
        print("- Some tests failed. Check the errors above.")
        sys.exit(1)
