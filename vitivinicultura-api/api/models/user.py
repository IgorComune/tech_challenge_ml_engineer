"""
Defines the Pydantic schema used for user input validation.
"""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    Schema for creating a new user via API.

    Attributes:
        username (str): Desired username.
        password (str): Plaintext password to be hashed.
    """

    username: str
    password: str
