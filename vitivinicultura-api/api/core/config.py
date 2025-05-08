from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.
    ---
    Attributes:
        SECRET_KEY (str): Secret key used to sign JWT tokens.
        ALGORITHM (str): Algorithm used for JWT signing (default: HS256).
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Token expiration time in minutes.
        DEBUG (bool): Enables FastAPI debug mode if set to True.
    """

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
