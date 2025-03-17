class ProjectNotFoundException(Exception):
    "Exception used for failed project search."
    
    def __init__(self, message: str = "Project not found."):
        self.message = message

    def __str__(self):
        return self.message

class UpdateProjectException(Exception):
    "Exception used for failed project update."

    def __init__(self, message: str = "Error while parsing update data."):
        self.message = message

    def __str__(self):
        return self.message
