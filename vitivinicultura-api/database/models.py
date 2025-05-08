"""
Defines the SQLAlchemy ORM models used in the application.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    ORM model for users.

    Attributes:
        id (int): Primary key, unique identifier for each user.
        username (str): Unique username.
        hashed_password (str): Hashed version of the user's password.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
