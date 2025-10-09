from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.content import Service, FAQ
from app.schemas.content import (
    ServiceCreate, ServiceUpdate, ServiceResponse,
    FAQCreate, FAQUpdate, FAQResponse
)
from app.utils.security import get_current_active_user, require_roles
from app.utils.audit import log_audit_event, get_client_ip, get_user_agent
from app.services.cache_service import cache_service
from typing import List

router = APIRouter(prefix="/content", tags=["content"])


# Services endpoints
@router.get("/services", response_model=List[ServiceResponse])
async def get_services(
    db: Session = Depends(get_db)
):
    """Get all active services."""
    # Try cache first
    cache_key = cache_service.generate_key("services", "active")
    cached_services = await cache_service.get(cache_key)
    
    if cached_services:
        return cached_services
    
    # Get from database
    services = db.query(Service).filter(Service.is_active == True).order_by(Service.order).all()
    
    # Cache for 1 hour
    await cache_service.set(cache_key, services, ttl=3600)
    
    return services


@router.post("/services", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: ServiceCreate,
    request: Request,
    current_user: User = Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    """Create a new service (admin only)."""
    service = Service(**service_data.dict())
    
    db.add(service)
    db.commit()
    db.refresh(service)
    
    # Clear cache
    await cache_service.delete(cache_service.generate_key("services", "active"))
    
    # Log audit event
    log_audit_event(
        db=db,
        user=current_user,
        action="create_service",
        resource="service",
        resource_id=str(service.id),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return service


@router.put("/services/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    service_data: ServiceUpdate,
    request: Request,
    current_user: User = Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    """Update a service (admin only)."""
    service = db.query(Service).filter(Service.id == service_id).first()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Update fields
    for field, value in service_data.dict(exclude_unset=True).items():
        setattr(service, field, value)
    
    db.commit()
    db.refresh(service)
    
    # Clear cache
    await cache_service.delete(cache_service.generate_key("services", "active"))
    
    # Log audit event
    log_audit_event(
        db=db,
        user=current_user,
        action="update_service",
        resource="service",
        resource_id=str(service.id),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return service


@router.delete("/services/{service_id}")
async def delete_service(
    service_id: int,
    request: Request,
    current_user: User = Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    """Delete a service (admin only)."""
    service = db.query(Service).filter(Service.id == service_id).first()
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    db.delete(service)
    db.commit()
    
    # Clear cache
    await cache_service.delete(cache_service.generate_key("services", "active"))
    
    # Log audit event
    log_audit_event(
        db=db,
        user=current_user,
        action="delete_service",
        resource="service",
        resource_id=str(service_id),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return {"message": "Service deleted successfully"}


# FAQ endpoints
@router.get("/faq", response_model=List[FAQResponse])
async def get_faqs(
    category: str = None,
    db: Session = Depends(get_db)
):
    """Get all active FAQs, optionally filtered by category."""
    # Try cache first
    cache_key = cache_service.generate_key("faqs", "active", category or "all")
    cached_faqs = await cache_service.get(cache_key)
    
    if cached_faqs:
        return cached_faqs
    
    # Get from database
    query = db.query(FAQ).filter(FAQ.is_active == True)
    
    if category:
        query = query.filter(FAQ.category == category)
    
    faqs = query.order_by(FAQ.order).all()
    
    # Cache for 1 hour
    await cache_service.set(cache_key, faqs, ttl=3600)
    
    return faqs


@router.post("/faq", response_model=FAQResponse, status_code=status.HTTP_201_CREATED)
async def create_faq(
    faq_data: FAQCreate,
    request: Request,
    current_user: User = Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    """Create a new FAQ (admin only)."""
    faq = FAQ(**faq_data.dict())
    
    db.add(faq)
    db.commit()
    db.refresh(faq)
    
    # Clear cache
    await cache_service.delete(cache_service.generate_key("faqs", "active", "all"))
    if faq.category:
        await cache_service.delete(cache_service.generate_key("faqs", "active", faq.category))
    
    # Log audit event
    log_audit_event(
        db=db,
        user=current_user,
        action="create_faq",
        resource="faq",
        resource_id=str(faq.id),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return faq


@router.put("/faq/{faq_id}", response_model=FAQResponse)
async def update_faq(
    faq_id: int,
    faq_data: FAQUpdate,
    request: Request,
    current_user: User = Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    """Update a FAQ (admin only)."""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    
    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ not found"
        )
    
    # Update fields
    for field, value in faq_data.dict(exclude_unset=True).items():
        setattr(faq, field, value)
    
    db.commit()
    db.refresh(faq)
    
    # Clear cache
    await cache_service.delete(cache_service.generate_key("faqs", "active", "all"))
    if faq.category:
        await cache_service.delete(cache_service.generate_key("faqs", "active", faq.category))
    
    # Log audit event
    log_audit_event(
        db=db,
        user=current_user,
        action="update_faq",
        resource="faq",
        resource_id=str(faq.id),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return faq


@router.delete("/faq/{faq_id}")
async def delete_faq(
    faq_id: int,
    request: Request,
    current_user: User = Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    """Delete a FAQ (admin only)."""
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    
    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ not found"
        )
    
    category = faq.category
    db.delete(faq)
    db.commit()
    
    # Clear cache
    await cache_service.delete(cache_service.generate_key("faqs", "active", "all"))
    if category:
        await cache_service.delete(cache_service.generate_key("faqs", "active", category))
    
    # Log audit event
    log_audit_event(
        db=db,
        user=current_user,
        action="delete_faq",
        resource="faq",
        resource_id=str(faq_id),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return {"message": "FAQ deleted successfully"}
