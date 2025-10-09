from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.database import get_async_mongo_collection
from app.schemas.chat import (
    ChatMessageCreate, ChatMessageResponse, ChatSessionResponse,
    SymptomAnalysisRequest, SymptomAnalysisResponse, ChatResponse
)
from app.services.gemini_service import GeminiAIService
from app.services.cache_service import cache_service
from app.services.mcp_chatbot import MCPChatbotService  # Update the path if the module is located elsewhere
gemini_service = GeminiAIService()
mcp_chatbot = MCPChatbotService()  # Initialize MCPChatbotService
from app.utils.security_simple import get_current_active_user
from app.utils.rate_limiter import strict_rate_limiter
from app.utils.audit_simple import log_audit_event, get_client_ip, get_user_agent
from datetime import datetime
import uuid
from typing import Optional

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/symptom", response_model=SymptomAnalysisResponse)
async def analyze_symptoms(
    request_data: SymptomAnalysisRequest,
    request: Request,
    current_user = Depends(get_current_active_user)
):
    """Analyze symptoms and provide medical insights using MCP chatbot."""
    try:
        # Convert request to dict for MCP chatbot
        analysis_data = request_data.dict()
        
        # Generate cache key
        cache_key = cache_service.generate_key(
            "symptom_analysis",
            str(current_user["id"]),
            hash(str(sorted(request_data.symptoms)))
        )
        
        # Try to get from cache first
        cached_result = await cache_service.get(cache_key)
        if cached_result:
            return SymptomAnalysisResponse(**cached_result)
        
        # Analyze symptoms using Gemini
        result = await gemini_service.analyze_symptoms(analysis_data)
        
        # Cache the result for 1 hour
        await cache_service.set(cache_key, result.dict(), ttl=3600)
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze symptoms: {str(e)}"
        )


@router.post("/session", response_model=ChatSessionResponse)
async def create_chat_session(
    current_user = Depends(get_current_active_user)
):
    """Create a new chat session."""
    session_id = str(uuid.uuid4())
    
    # Create session in MongoDB
    chat_collection = get_async_mongo_collection("chat_sessions")
    session_data = {
        "session_id": session_id,
        "user_id": str(current_user["id"]),
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "messages": []
    }
    
    result = await chat_collection.insert_one(session_data)
    
    return ChatSessionResponse(
        id=str(result.inserted_id),
        session_id=session_id,
        user_id=str(current_user["id"]),
        is_active=True,
        created_at=session_data["created_at"],
        updated_at=session_data["updated_at"]
    )


@router.get("/sessions", response_model=list[ChatSessionResponse])
async def get_chat_sessions(
    current_user = Depends(get_current_active_user)
):
    """Get user's chat sessions."""
    chat_collection = get_async_mongo_collection("chat_sessions")
    sessions = await chat_collection.find(
        {"user_id": str(current_user["id"])}
    ).sort("created_at", -1).to_list(length=None)
    
    return [
        ChatSessionResponse(
            id=str(session["_id"]),
            session_id=session["session_id"],
            user_id=session["user_id"],
            is_active=session["is_active"],
            created_at=session["created_at"],
            updated_at=session["updated_at"]
        )
        for session in sessions
    ]


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str,
    current_user = Depends(get_current_active_user)
):
    """Get a specific chat session with messages."""
    chat_collection = get_async_mongo_collection("chat_sessions")
    session = await chat_collection.find_one({
        "session_id": session_id,
        "user_id": str(current_user["id"])
    })
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    return ChatSessionResponse(
        id=str(session["_id"]),
        session_id=session["session_id"],
        user_id=session["user_id"],
        is_active=session["is_active"],
        created_at=session["created_at"],
        updated_at=session["updated_at"]
    )


@router.post("/sessions/{session_id}/messages", response_model=ChatResponse)
async def send_message(
    session_id: str,
    message_data: ChatMessageCreate,
    request: Request,
    current_user = Depends(get_current_active_user)
):
    """Send a message in a chat session using MCP chatbot."""
    try:
        # Process message using MCP chatbot
        response = await mcp_chatbot.process_chat_message(
            message=message_data.content,
            user_id=str(current_user["id"]),
            session_id=session_id
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )


@router.delete("/sessions/{session_id}")
async def end_chat_session(
    session_id: str,
    current_user = Depends(get_current_active_user)
):
    """End a chat session."""
    chat_collection = get_async_mongo_collection("chat_sessions")
    
    result = await chat_collection.update_one(
        {
            "session_id": session_id,
            "user_id": str(current_user["id"])
        },
        {
            "$set": {
                "is_active": False,
                "ended_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    return {"message": "Chat session ended successfully"}
