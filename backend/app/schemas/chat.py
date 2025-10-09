from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatMessageBase(BaseModel):
    content: str
    message_type: str = "user"


class ChatMessage(ChatMessageBase):
    id: str
    session_id: str
    is_ai_generated: bool
    message_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime


class ChatMessageCreate(ChatMessageBase):
    session_id: Optional[str] = None


class ChatMessageResponse(ChatMessageBase):
    id: int
    session_id: int
    is_ai_generated: bool
    message_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionResponse(BaseModel):
    id: str
    session_id: str
    user_id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    message: str
    session_id: str
    timestamp: datetime
    is_medical: bool = False
    confidence: float = 0.0


class SymptomAnalysisRequest(BaseModel):
    symptoms: List[str]
    age: Optional[int] = None
    gender: Optional[str] = None
    medical_history: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None
    additional_info: Optional[str] = None


class Condition(BaseModel):
    name: str
    probability: float
    description: str
    severity: str


class TriageAdvice(BaseModel):
    urgency: str  # low, medium, high, emergency
    recommendation: str
    timeframe: str


class SymptomAnalysisResponse(BaseModel):
    conditions: List[Condition]
    triage_advice: TriageAdvice
    disclaimer: str
    confidence_score: float
    follow_up_recommendations: List[str]
