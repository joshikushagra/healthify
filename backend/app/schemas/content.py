from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ServiceBase(BaseModel):
    title: str
    description: Optional[str] = None
    icon: Optional[str] = None
    price: Optional[str] = None
    duration: Optional[str] = None
    is_active: bool = True
    order: int = 0
    service_metadata: Optional[Dict[str, Any]] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    price: Optional[str] = None
    duration: Optional[str] = None
    is_active: Optional[bool] = None
    order: Optional[int] = None
    service_metadata: Optional[Dict[str, Any]] = None


class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FAQBase(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None
    is_active: bool = True
    order: int = 0


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None
    order: Optional[int] = None


class FAQResponse(FAQBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
