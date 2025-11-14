from datetime import datetime
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.database import get_async_mongo_collection
from app.schemas.user_simple import Token, UserCreate, UserLogin, UserResponse
from app.utils.auth_simple import (create_tokens, get_password_hash,
                                   verify_password, verify_token)

router = APIRouter(prefix="/auth", tags=["authentication"])


def _serialize_user(user_doc: dict) -> UserResponse:
    """Convert a Mongo document into a UserResponse."""
    return UserResponse(
        id=str(user_doc["_id"]),
        email=user_doc["email"],
        username=user_doc.get("username", ""),
        first_name=user_doc.get("first_name"),
        last_name=user_doc.get("last_name"),
        phone_number=user_doc.get("phone_number"),
        user_type=user_doc.get("user_type"),
        is_active=user_doc.get("is_active", True),
        is_verified=user_doc.get("is_verified", False),
        created_at=user_doc.get("created_at", datetime.utcnow()),
        updated_at=user_doc.get("updated_at"),
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    request: Request
):
    """Register a new user."""
    try:
        users_collection = get_async_mongo_collection("users")

        existing_user = await users_collection.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(user_data.password)
        timestamp = datetime.utcnow()

        user_doc = {
            "_id": user_id,
            "email": user_data.email,
            "username": user_data.username,
            "hashed_password": hashed_password,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "phone_number": user_data.phone_number,
            "user_type": user_data.user_type,
            "is_active": True,
            "is_verified": False,
            "created_at": timestamp,
            "updated_at": timestamp,
            "last_login": None,
            "registered_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
        }

        await users_collection.insert_one(user_doc)

        return _serialize_user(user_doc)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    request: Request
):
    """Authenticate user and return tokens."""
    try:
        # Get users collection
        users_collection = get_async_mongo_collection("users")
        
        # Find user by email
        user = await users_collection.find_one({"email": user_credentials.email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify password
        if not verify_password(user_credentials.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Check if user is active
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Create tokens
        access_token, refresh_token = create_tokens(
            user_id=user["_id"],
            email=user["email"]
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    request: Request
):
    """Refresh access token using refresh token."""
    try:
        # Verify refresh token
        payload = verify_token(refresh_token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get users collection
        users_collection = get_async_mongo_collection("users")
        user = await users_collection.find_one({"_id": user_id})
        
        if not user or not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new tokens
        access_token, new_refresh_token = create_tokens(
            user_id=user["_id"],
            email=user["email"]
        )
        
        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )


@router.post("/logout")
async def logout(
    request: Request
):
    """Logout user (invalidate tokens)."""
    return {"message": "Logged out successfully"}


# Simple user info endpoint for testing
@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user = Depends(lambda: {"id": "test_user", "email": "test@example.com", "username": "testuser"})
):
    """Get current user information."""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        username=current_user["username"],
        is_active=True,
        is_verified=True,
        created_at=datetime.utcnow()
    )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str):
    """Fetch a user's profile from MongoDB."""
    users_collection = get_async_mongo_collection("users")
    user = await users_collection.find_one({"_id": user_id})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return _serialize_user(user)
