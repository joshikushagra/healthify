#!/usr/bin/env python3
"""
Database setup script for Healthify backend
Run this after installing PostgreSQL
"""

import os
import sys
from sqlalchemy import create_engine, text
from app.config import settings

def setup_database():
    """Set up the database and run migrations"""
    try:
        print("🗄️  Setting up Healthify database...")
        
        # Create engine
        engine = create_engine(settings.database_url)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {version}")
        
        # Create tables
        print("📋 Creating database tables...")
        from app.database import Base
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Run Alembic migrations
        print("🔄 Running database migrations...")
        import subprocess
        result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database migrations completed!")
        else:
            print(f"⚠️  Migration warning: {result.stderr}")
        
        print("\n🎉 Database setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Start the server: py -m uvicorn app.main:app --reload")
        print("2. Access API docs: http://localhost:8000/docs")
        print("3. Test health endpoint: http://localhost:8000/health")
        
    except Exception as e:
        print(f"❌ Database setup failed: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your DATABASE_URL in .env file")
        print("3. Verify database and user exist")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()
