"""
Authentication and user creation route:
    receives username and password, create it, validates credentials,
    and returns a JWT token if successful.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from api.core.security import (
    verify_password,
    create_access_token,
    hash_password,
)
from api.core.config import settings
from api.models.user import UserCreate
from database.db import SessionLocal
from database.models import User


router = APIRouter(prefix="/auth", tags=["auth"])

# Temporary in-memory user store for testing
# hashed = hash_password("secret123")
# fake_users_db = {
#    "yuri": {
#        "username": "yuri",
#        "hashed_password": hashed
#    }
# }


def get_db():
    """
    Dependency that provides a database session.

    Yields:
        Session: SQLAlchemy session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user by storing their credentials in the database.

    Args:
        user (UserCreate): The user data submitted in the request body.
        db (Session): The database session.

    Raises:
        HTTPException: If the username already exists.

    Returns:
        dict: A confirmation message with the new user's username and ID.
    """
    existing_user = (
        db.query(User).filter(User.username == user.username).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )

    new_user = User(
        username=user.username, hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"username": new_user.username, "id": new_user.id}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticates a user using form credentials against the database.

    Args:
        form_data (OAuth2PasswordRequestForm): Contains username and password.
        db (Session): SQLAlchemy DB session.

    Returns:
        dict: JWT token and token type.

    Raises:
        HTTPException: If credentials are invalid.
    """
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid username or password"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401, detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    return {"access_token": access_token, "token_type": "bearer"}
