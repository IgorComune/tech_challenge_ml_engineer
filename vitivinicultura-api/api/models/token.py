from pydantic import BaseModel


class TokenResponse(BaseModel):
    """
    Schema for returning an access token after successful authentication.

    Attributes:
        access_token (str): JWT used for authenticating subsequent requests.
        token_type (str): Type of the token, typically "bearer".
        expires_in (int | None): Optional. Minutes until the token expires.
    """

    access_token: str
    token_type: str
    expires_in: int | None = None
