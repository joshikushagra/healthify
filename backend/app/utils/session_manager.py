from datetime import datetime, timedelta
from typing import Optional, Dict
from app.database_manager import db_manager
import uuid
import structlog

logger = structlog.get_logger()

class SessionManager:
    def __init__(self):
        self.collection_name = "user_sessions"
        self.db = db_manager.get_async_db()
        
    async def create_session(self, user_id: str, device_info: Dict) -> str:
        """Create a new session for a user."""
        session_id = str(uuid.uuid4())
        session = {
            "_id": session_id,
            "user_id": user_id,
            "device_info": device_info,
            "created_at": datetime.utcnow(),
            "last_active": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=30),
            "is_active": True
        }
        
        await self.db[self.collection_name].insert_one(session)
        return session_id
    
    async def validate_session(self, session_id: str) -> Optional[Dict]:
        """Validate and update a session."""
        session = await self.db[self.collection_name].find_one({
            "_id": session_id,
            "is_active": True,
            "expires_at": {"$gt": datetime.utcnow()}
        })
        
        if session:
            await self.update_last_active(session_id)
            return session
        return None
    
    async def update_last_active(self, session_id: str):
        """Update the last active timestamp of a session."""
        await self.db[self.collection_name].update_one(
            {"_id": session_id},
            {
                "$set": {
                    "last_active": datetime.utcnow()
                }
            }
        )
    
    async def end_session(self, session_id: str):
        """End a user session."""
        await self.db[self.collection_name].update_one(
            {"_id": session_id},
            {
                "$set": {
                    "is_active": False,
                    "ended_at": datetime.utcnow()
                }
            }
        )
    
    async def end_all_sessions(self, user_id: str, except_session_id: Optional[str] = None):
        """End all sessions for a user except the current one."""
        query = {
            "user_id": user_id,
            "is_active": True
        }
        if except_session_id:
            query["_id"] = {"$ne": except_session_id}
            
        await self.db[self.collection_name].update_many(
            query,
            {
                "$set": {
                    "is_active": False,
                    "ended_at": datetime.utcnow()
                }
            }
        )
    
    async def get_active_sessions(self, user_id: str) -> list:
        """Get all active sessions for a user."""
        return await self.db[self.collection_name].find({
            "user_id": user_id,
            "is_active": True,
            "expires_at": {"$gt": datetime.utcnow()}
        }).to_list(None)

# Create global instance
session_manager = SessionManager()