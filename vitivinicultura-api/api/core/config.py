from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.

    Attributes:
        ALGORITHM (str): JWT signing algorithm.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Expiration duration access tokens.
        DATABASE_URL (str): Database connection string.
        DEBUG (bool): Enables FastAPI debug mode if True.
        SECRET_KEY (str): Used to sign JWT tokens.
    """

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./database/users.db"
    DEBUG: bool = True
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
