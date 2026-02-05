from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter
from slowapi.util import get_remote_address
from config.settings import settings
import secrets

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    
    Args:
        data: Data to encode in token
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token data
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def generate_session_token() -> str:
    """Generate secure random session token"""
    return secrets.token_urlsafe(32)

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """
    Dependency to extract and validate bearer token
    
    Returns:
        Token string
    """
    return credentials.credentials

def validate_input(data: str, max_length: int = 1000, allow_special_chars: bool = False) -> bool:
    """
    Validate user input for security
    
    Args:
        data: Input string to validate
        max_length: Maximum allowed length
        allow_special_chars: Whether to allow special characters
        
    Returns:
        True if valid
        
    Raises:
        HTTPException: If validation fails
    """
    if len(data) > max_length:
        raise HTTPException(status_code=400, detail=f"Input exceeds maximum length of {max_length}")
    
    if not allow_special_chars:
        # Basic SQL injection and XSS prevention
        dangerous_chars = ["<", ">", "script", "SELECT", "DROP", "INSERT", "DELETE", "UPDATE"]
        for char in dangerous_chars:
            if char.lower() in data.lower():
                raise HTTPException(status_code=400, detail="Invalid characters in input")
    
    return True

class RateLimitMiddleware:
    """Rate limiting middleware"""
    
    @staticmethod
    @limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
    async def check_rate_limit(request: Request):
        """Check if request is within rate limit"""
        pass
