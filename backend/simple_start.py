#!/usr/bin/env python3
"""
Simple startup script for Healthify backend without MongoDB dependency.
This script starts the FastAPI server with basic functionality.
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

def start_server():
    """Start the FastAPI server."""
    try:
        print("Starting Healthify Backend (Simple Mode)")
        print("=" * 50)
        print("Starting with simple settings; ensure MongoDB is running for full features")
        print("To enable full functionality:")
        print("   1. Install MongoDB: https://www.mongodb.com/try/download/community")
        print("   2. Start MongoDB: mongod --dbpath C:\\data\\db")
        print("   3. Set your API keys in environment variables")
        print("=" * 50)
        
        import uvicorn
        from app.main import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"Failed to start server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements-simple.txt")
        print("2. Check if port 8000 is available")
        print("3. Verify Python version (3.11+ required)")
        sys.exit(1)

if __name__ == "__main__":
    start_server()
