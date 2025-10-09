#!/usr/bin/env python3
"""
SQLite database setup script for Healthify backend
This is easier for development than PostgreSQL
"""

import os
import sys
from sqlalchemy import create_engine
from app.database_sqlite import Base, engine

def setup_sqlite_database():
    """Set up SQLite database and create tables"""
    try:
        print("🗄️  Setting up Healthify SQLite database...")
        
        # Create all tables
        print("📋 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        print("\n🎉 SQLite database setup completed!")
        print(f"📁 Database file: {os.path.abspath('healthify.db')}")
        print("\n📋 Next steps:")
        print("1. Update your .env file to use SQLite")
        print("2. Start the server: py -m uvicorn app.main:app --reload")
        print("3. Access API docs: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Database setup failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    setup_sqlite_database()
