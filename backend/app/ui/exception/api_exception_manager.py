from http import HTTPStatus

from app.application.domain.exception import (
    AuthenticationError, ConflictError, ForbiddenError,
    NotFoundError, RepositoryError, ValidationError
)
from .api_error import APIError
from app.utils import Messages

class APIExceptionManager:
    @staticmethod
    def build(err: Exception) -> APIError:
        if type(err).__name__ == "ValidationError":
            msg = getattr(err, "messages", str(err))
            return APIError(HTTPStatus.BAD_REQUEST, Messages.Validation.INVALID_DATA, str(msg))

        if isinstance(err, AuthenticationError):
            return APIError(HTTPStatus.UNAUTHORIZED, err.message, err.description)
        if isinstance(err, ForbiddenError):
            return APIError(HTTPStatus.FORBIDDEN, err.message, err.description)
        if isinstance(err, ValidationError):
            return APIError(HTTPStatus.BAD_REQUEST, err.message, err.description)
        if isinstance(err, NotFoundError):
            return APIError(HTTPStatus.NOT_FOUND, err.message, err.description)
        if isinstance(err, ConflictError):
            return APIError(HTTPStatus.CONFLICT, err.message, err.description)
        if isinstance(err, RepositoryError):
            return APIError(HTTPStatus.INTERNAL_SERVER_ERROR, err.message, err.description)

        return APIError(HTTPStatus.INTERNAL_SERVER_ERROR, Messages.Generic.INTERNAL_ERROR, str(err))
