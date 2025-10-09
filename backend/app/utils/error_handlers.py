from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Dict, Any
import structlog
import uuid

logger = structlog.get_logger()

class APIException(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str = None,
        details: Dict[str, Any] = None
    ):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)

async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for the API."""
    request_id = str(uuid.uuid4())
    
    if isinstance(exc, APIException):
        logger.error("API error",
            request_id=request_id,
            path=request.url.path,
            error_code=exc.error_code,
            status_code=exc.status_code,
            message=exc.message,
            details=exc.details
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
                "error_code": exc.error_code,
                "details": exc.details,
                "request_id": request_id
            }
        )
    
    # Handle unexpected errors
    logger.error("Unexpected error",
        request_id=request_id,
        path=request.url.path,
        error=str(exc),
        error_type=type(exc).__name__
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "request_id": request_id
        }
    )