class UserNotFoundException(Exception):
    "Exception used for failed user search."

    message = "User not found."

    def __init__(self, message: str):
        self.message = message