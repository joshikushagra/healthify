from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.utils.auth import verify_password, get_password_hash, create_tokens, verify_token
from app.utils.audit import log_audit_event, get_client_ip, get_user_agent
from app.utils.rate_limiter import rate_limiter
from app.utils.security import get_current_user
from datetime import datetime
import uuid

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        phone_number=user_data.phone_number,
        date_of_birth=user_data.date_of_birth
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Log audit event
    log_audit_event(
        db=db,
        user=db_user,
        action="register",
        resource="user",
        resource_id=str(db_user.id),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return db_user


@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """Login user and return tokens."""
    # Find user
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create tokens
    tokens = create_tokens(user.id, user.email, user.role.value)
    
    # Log audit event
    log_audit_event(
        db=db,
        user=user,
        action="login",
        resource="user",
        resource_id=str(user.id),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return tokens


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    try:
        # Verify refresh token
        token_data = verify_token(refresh_token, "refresh")
        
        # Get user
        user = db.query(User).filter(User.id == token_data.user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new tokens
        tokens = create_tokens(user.id, user.email, user.role.value)
        
        # Log audit event
        log_audit_event(
            db=db,
            user=user,
            action="token_refresh",
            resource="user",
            resource_id=str(user.id),
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request)
        )
        
        return tokens
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile."""
    return current_user


@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout user (client should discard tokens)."""
    # Log audit event
    log_audit_event(
        db=db,
        user=current_user,
        action="logout",
        resource="user",
        resource_id=str(current_user.id),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return {"message": "Successfully logged out"}


