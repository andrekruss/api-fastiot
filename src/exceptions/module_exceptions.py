class ModuleNotFoundException(Exception):
    "Exception used for failed module search."
    
    def __init__(self, message: str = "Module not found."):
        self.message = message

    def __str__(self):
        return self.message

class BadUpdateDataException(Exception):
    "Exception used for failed module update."

    def __init__(self, message: str = "Failed parsing update data"):
        self.message = message

    def __str__(self):
        return self.message