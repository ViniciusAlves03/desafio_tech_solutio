from app.application.domain.exception import Error

class APIError(Error):
    def __init__(self, code: int, message: str, description: str = ""):
        super().__init__(message, description)
        self.code = code

    def toJSON(self) -> dict:
        result = {
            "code": self.code,
            "message": self.message
        }
        if self.description:
            result["description"] = self.description
        return result
