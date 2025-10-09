from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from app.models.user import User
from typing import Optional
import json


def log_audit_event(
    db: Session,
    user: Optional[User],
    action: str,
    resource: str,
    resource_id: Optional[str] = None,
    details: Optional[dict] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """Log an audit event to the database."""
    audit_log = AuditLog(
        user_id=user.id if user else None,
        action=action,
        resource=resource,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.add(audit_log)
    db.commit()


def get_client_ip(request) -> str:
    """Extract client IP address from request."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host


def get_user_agent(request) -> str:
    """Extract user agent from request."""
    return request.headers.get("User-Agent", "")
