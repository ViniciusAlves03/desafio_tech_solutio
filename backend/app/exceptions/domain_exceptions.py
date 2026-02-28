class Error(Exception):
    def __init__(self, message: str, description: str = ""):
        super().__init__(message)
        self.message = message
        self.description = description

class AuthenticationError(Error):
    pass

class ForbiddenError(Error):
    pass

class ValidationError(Error):
    pass

class NotFoundError(Error):
    pass

class ConflictError(Error):
    pass

class RepositoryError(Error):
    pass
