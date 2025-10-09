from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.content_simple import ContentCreate, ContentResponse
from datetime import datetime
import uuid

router = APIRouter(prefix="/content", tags=["content"])


@router.get("/", response_model=list[ContentResponse])
async def get_content():
    """Get all content (simplified)."""
    # Return sample content
    return [
        ContentResponse(
            id="1",
            title="Welcome to Healthify",
            content="This is a sample medical content article.",
            category="general",
            created_at=datetime.utcnow()
        )
    ]


@router.post("/", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def create_content(content_data: ContentCreate):
    """Create new content (simplified)."""
    content_id = str(uuid.uuid4())
    return ContentResponse(
        id=content_id,
        title=content_data.title,
        content=content_data.content,
        category=content_data.category,
        created_at=datetime.utcnow()
    )
