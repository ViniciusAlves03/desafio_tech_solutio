class APIException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ValidationException(APIException):
    def __init__(self, message: str = "Dados inválidos ou incompletos."):
        super().__init__(message, status_code=400)

class UnauthorizedException(APIException):
    def __init__(self, message: str = "Credenciais incorretas ou acesso não autorizado."):
        super().__init__(message, status_code=401)

class ForbiddenException(APIException):
    def __init__(self, message: str = "Acesso negado. Permissão insuficiente."):
        super().__init__(message, status_code=403)

class NotFoundException(APIException):
    def __init__(self, message: str = "Recurso não encontrado."):
        super().__init__(message, status_code=404)

class ConflictException(APIException):
    def __init__(self, message: str = "Conflito de dados. O recurso já existe."):
        super().__init__(message, status_code=409)
