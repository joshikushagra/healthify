#!/usr/bin/env python3
"""
Simple test server to verify the setup works.
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Healthify Test Server")

@app.get("/")
async def root():
    return {"message": "Healthify Test Server is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Test server is working"}

if __name__ == "__main__":
    print("🚀 Starting Healthify Test Server")
    print("=" * 50)
    print("✅ Server will be available at: http://localhost:8000")
    print("✅ Health check: http://localhost:8000/health")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
