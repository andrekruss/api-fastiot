class UserNotFoundException(Exception):
    "Exception used for failed user search."
    
    def __init__(self, message: str = "User not found."):
        self.message = message

    def __str__(self):
        return self.message

class UserConflictException(Exception):
    "Exception used for user conflict."
    
    def __init__(self, message: str = "User with informed email or username already exists."):
        self.message = message

    def __str__(self):
        return self.message
