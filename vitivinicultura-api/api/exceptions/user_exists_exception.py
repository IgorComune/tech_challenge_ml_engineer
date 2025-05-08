class UserExistsException(Exception):
    """
    Raised when attempting to register a user that already exists.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message: str = "User already exists"):
        self.message = message
        super().__init__(self.message)
