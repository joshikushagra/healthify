from celery import current_task
from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models.chat import ChatSession
from app.models.user import User
from app.config import settings
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@current_task.task
def cleanup_expired_sessions():
    """Clean up expired chat sessions."""
    db = SessionLocal()
    try:
        # Find sessions older than 24 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        expired_sessions = db.query(ChatSession).filter(
            ChatSession.created_at < cutoff_time,
            ChatSession.is_active == True
        ).all()
        
        for session in expired_sessions:
            session.is_active = False
            session.ended_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        return f"Cleaned up {len(expired_sessions)} expired sessions"
        
    except Exception as e:
        logger.error(f"Error cleaning up sessions: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


@current_task.task
def send_reminder_emails():
    """Send reminder emails to users."""
    # This would integrate with your email service
    # For now, just log the task
    logger.info("Sending reminder emails")
    return "Reminder emails sent"


@current_task.task
def process_ai_request_async(user_id: int, request_data: dict):
    """Process AI request asynchronously."""
    from app.services.ai_service import ai_service
    
    try:
        # Process the AI request
        result = ai_service.analyze_symptoms(request_data)
        
        # Store result in cache or database
        # This is a placeholder - implement based on your needs
        
        logger.info(f"Processed AI request for user {user_id}")
        return "AI request processed successfully"
        
    except Exception as e:
        logger.error(f"Error processing AI request: {str(e)}")
        raise
