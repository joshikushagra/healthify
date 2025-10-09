from fastapi import APIRouter, Depends
from app.database_manager import db_manager
from app.services.gemini_service import GeminiAIService
from typing import Dict
import time

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check() -> Dict:
    """
    Comprehensive health check endpoint.
    Checks database, AI service, and overall API health.
    """
    start_time = time.time()
    
    # Check database
    db_healthy = await db_manager.health_check()
    
    # Check AI service
    ai_service = GeminiAIService()
    ai_healthy = await ai_service.health_check()
    
    # Calculate response time
    response_time = time.time() - start_time
    
    return {
        "status": "healthy" if (db_healthy and ai_healthy) else "degraded",
        "timestamp": time.time(),
        "response_time_ms": round(response_time * 1000, 2),
        "services": {
            "database": {
                "status": "healthy" if db_healthy else "unhealthy",
                "type": "mongodb"
            },
            "ai_service": {
                "status": "healthy" if ai_healthy else "unhealthy",
                "type": "gemini"
            }
        },
        "version": "1.0.0"
    }

@router.get("/health/db")
async def database_health() -> Dict:
    """Database-specific health check."""
    healthy = await db_manager.health_check()
    return {
        "status": "healthy" if healthy else "unhealthy",
        "timestamp": time.time(),
        "service": "mongodb"
    }

@router.get("/health/ai")
async def ai_service_health() -> Dict:
    """AI service health check."""
    ai_service = GeminiAIService()
    healthy = await ai_service.health_check()
    return {
        "status": "healthy" if healthy else "unhealthy",
        "timestamp": time.time(),
        "service": "gemini"
    }