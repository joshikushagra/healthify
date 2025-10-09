from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ContentCreate(BaseModel):
    title: str
    content: str
    category: str


class ContentResponse(BaseModel):
    id: str
    title: str
    content: str
    category: str
    created_at: datetime
