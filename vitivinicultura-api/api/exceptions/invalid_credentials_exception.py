class InvalidCredentialsException(Exception):
    """
    Raised when a user provides invalid credentials during authentication.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message: str = "Invalid credentials"):
        self.message = message
        super().__init__(self.message)
