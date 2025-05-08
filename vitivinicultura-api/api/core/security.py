"""
Security utilities for password hashing, token generation, and
user authentication.
---
Uses:
- passlib (bcrypt) for secure password hashing and verification.
- python-jose for JWT token creation and decoding.
- FastAPI OAuth2PasswordBearer to extract tokens from requests.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from api.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Password hash and verification


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    ---
    Argument:
        password (str): The raw password input.

    Return:
        str: A securely hashed password.
    """

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    ---
    Arguments:
        plain_password (str): The password provided by the user.
        hashed_password (str): The stored hashed password to compare with.

    Returns:
        bool: True if the password matches, False otherwise.
    """

    return pwd_context.verify(plain_password, hashed_password)


# JWT Token Creation


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a signed JWT access token.
    ---
    Arguments:
        data (dict): The payload data to include in the token
            (e.g., {"sub": username}).
        expires_delta (Optional[timedelta]):
            Optional expiration time for the token.

    Returns:
        str: A JWT string.
    """

    to_encode = data.copy()
    if isinstance(expires_delta, int):
        expires_delta = timedelta(minutes=expires_delta)
    elif expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )


# TokenData model used for validation
class TokenData(BaseModel):
    """
    Pydantic model for holding token payload data.
    ---
    Attributes:
        username (Optional[str]):
            The 'sub' field from the JWT, representing the user.
    """

    username: Optional[str] = None


# User validation


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependency to extract and validate the current user from the JWT token.
    ---
    Argument:
        token (str): JWT token extracted from the request header.

    Return:
        str: The username (sub) extracted from the token.

    Raise:
        HTTPException: If the token is missing, expired, or invalid.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
