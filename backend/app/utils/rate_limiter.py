from fastapi import HTTPException, Request, status
from app.database import get_async_mongo
from datetime import datetime, timedelta
from typing import Optional


class RateLimiter:
    def __init__(self, requests: int = 100, window: int = 60):
        self.requests = requests
        self.window = window
    
    async def __call__(self, request: Request):
        db = get_async_mongo()
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window)
        # Remove old entries
        await db.rate_limits.delete_many({"key": key, "timestamp": {"$lt": window_start}})
        # Count requests in window
        count = await db.rate_limits.count_documents({"key": key, "timestamp": {"$gte": window_start}})
        if count >= self.requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
        # Insert new request
        await db.rate_limits.insert_one({"key": key, "timestamp": now})
        return True


# Rate limiter instances
rate_limiter = RateLimiter(requests=100, window=60)
strict_rate_limiter = RateLimiter(requests=10, window=60)
