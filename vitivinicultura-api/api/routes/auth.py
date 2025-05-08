from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from database.db import get_db

from api.models.token import TokenResponse
from api.models.user import UserRequest, UserResponse
from api.services import auth_service
from api.exceptions.user_exists_exception import UserExistsException
from api.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRequest, db: Session = Depends(get_db)) -> UserResponse:
    """
    Endpoint to register a new user.

    Args:
        user (UserRequest): User input with username and password.
        db (Session): DB session (injected by FastAPI).

    Returns:
        UserResponse: Confirmation of new user creation.

    Raises:
        HTTPException: If the username is already taken.
    """
    try:
        return auth_service.register_user(user.username, user.password, db)
    except UserExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """
    Endpoint to authenticate a user and return a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form with username and password.
        db (Session): DB session (injected by FastAPI).

    Returns:
        JSONResponse: JWT access token and token type, with no-cache headers.

    Raises:
        HTTPException: If authentication fails.
    """
    try:
        token = auth_service.login_user(
            form_data.username, form_data.password, db
        )
        return JSONResponse(
            content=token.dict(),
            headers={
                "Cache-Control": "no-store",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
