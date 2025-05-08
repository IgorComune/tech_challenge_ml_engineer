"""
Provides the database engine, session, and initialization function.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.core.config import settings
from database.models import Base

# Use the configured database URL from settings
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initializes the database by creating all tables defined in SQLAlchemy models.
    This should be called at application startup.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency that provides a database session.
    Ensures that each request gets its own session,
    and that it is closed after use.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
