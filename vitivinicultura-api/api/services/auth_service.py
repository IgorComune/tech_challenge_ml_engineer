from sqlalchemy.orm import Session

from database.models import UserDB

from api.models.token import TokenResponse
from api.models.user import UserResponse
from api.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from api.exceptions.user_exists_exception import UserExistsException
from api.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)


def register_user(username: str, password: str, db: Session) -> UserResponse:
    """
    Handles user registration logic.
    - Checks if username already exists.
    - Hashes password and stores new user.

    Raises:
        UserExistsException: If username is taken.

    Returns:
        UserResponse: Username and ID of the newly created user.
    """
    if db.query(UserDB).filter_by(username=username).first():
        raise UserExistsException()

    new_user = UserDB(
        username=username,
        hashed_password=hash_password(password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(id=new_user.id, username=new_user.username)


def login_user(username: str, password: str, db: Session) -> TokenResponse:
    """
    Handles user login logic.
    - Verifies credentials.
    - Returns a JWT token on success.

    Raises:
        InvalidCredentialsException: If authentication fails.

    Returns:
        TokenResponse: JWT access token and token type.
    """
    user = db.query(UserDB).filter_by(username=username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentialsException()

    access_token = create_access_token(data={"sub": user.username})

    return TokenResponse(
        access_token=access_token, token_type="bearer", expires_in=3600
    )
