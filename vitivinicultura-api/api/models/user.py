"""
Defines the Pydantic schema used for user input validation.
"""

from pydantic import BaseModel


class UserRequest(BaseModel):
    """
    Schema for creating a new user via API.

    Attributes:
        username (str): Desired username.
        password (str): Plaintext password to be hashed.
    """

    username: str
    password: str


class UserResponse(BaseModel):
    """
    Schema for creating a new user via API.

    Attributes:
        username (str): Desired username.
        password (str): Plaintext password to be hashed.
    """

    id: int
    username: str
