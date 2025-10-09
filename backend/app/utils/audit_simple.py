from fastapi import Request
from typing import Optional

def log_audit_event(
    db=None,
    user=None,
    action: str = "",
    resource: str = "",
    resource_id: Optional[str] = None,
    details: Optional[dict] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """Log audit event (simplified - just print for now)."""
    print(f"Audit: {action} on {resource} by {user.get('id', 'unknown') if user else 'unknown'}")


def get_client_ip(request: Request) -> str:
    """Get client IP address."""
    return request.client.host if request.client else "unknown"


def get_user_agent(request: Request) -> str:
    """Get user agent."""
    return request.headers.get("user-agent", "unknown")
