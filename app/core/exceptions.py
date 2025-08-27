# app/core/exceptions.py
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from pydantic import BaseModel
import logging
import traceback
import uuid

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


# Response Models
class ValidationErrorDetail(BaseModel):
    field: str
    message: str
    type: str
    input: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    timestamp: datetime
    status_code: int
    path: Optional[str] = None
    message: str
    code: str
    details: Optional[str] = None
    field: Optional[str] = None
    request_id: Optional[str] = None
    stack_trace: Optional[str] = None
    environment: Optional[str] = None  # Added for environment context


class ValidationErrorResponse(BaseModel):
    success: bool = False
    timestamp: datetime
    status_code: int = 422
    path: Optional[str] = None
    message: str = "Validation failed"
    code: str = "VALIDATION_ERROR"
    validation_errors: List[ValidationErrorDetail]
    request_id: Optional[str] = None
    environment: Optional[str] = None


# Base Custom Exception
class BaseCustomException(HTTPException):
    """Base exception class for all custom exceptions"""

    def __init__(
        self,
        status_code: int,
        message: str,
        code: str,
        field: Optional[str] = None,
        details: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=status_code, detail=message, headers=headers)
        self.message = message
        self.code = code
        self.field = field
        self.details = details


# 400 - Bad Request Exceptions
class ValidationException(BaseCustomException):
    """For validation errors"""

    def __init__(
        self, message: str, field: Optional[str] = None, details: Optional[str] = None
    ):
        code = f"VALIDATION_ERROR_{field.upper()}" if field else "VALIDATION_ERROR"
        super().__init__(400, message, code, field, details)


class InvalidEmailException(ValidationException):
    """When email format is invalid"""

    def __init__(self, email: Optional[str] = None):
        if not email:
            message = "Email is required"
        elif "@" not in email:
            message = f"Invalid email format: {email}"
        else:
            message = f"Invalid email: {email}"
        super().__init__(message, "email")


class InvalidKeyIdException(ValidationException):
    """When keyid is invalid"""

    def __init__(self, keyid: Optional[str] = None):
        message = f"Invalid keyid: {keyid}" if keyid else "KeyId is required"
        super().__init__(message, "keyid")


# 401 - Unauthorized
class UnauthorizedException(BaseCustomException):
    """For authentication errors"""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(401, message, "UNAUTHORIZED")


# 403 - Forbidden
class ForbiddenException(BaseCustomException):
    """For authorization errors"""

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(403, message, "FORBIDDEN")


# 404 - Not Found Exceptions
class NotFoundExceptionBase(BaseCustomException):
    """Base for not found errors"""

    def __init__(
        self,
        resource: str,
        identifier: Optional[str] = None,
        details: Optional[str] = None,
    ):
        message = f"{resource} not found"
        if identifier:
            message = f"{resource} with identifier '{identifier}' not found"
        code = f"{resource.upper().replace(' ', '_')}_NOT_FOUND"
        super().__init__(404, message, code, details=details)


class SRNotFoundException(NotFoundExceptionBase):
    """When SR data is not found"""

    def __init__(self, sr_type: str, identifier: Optional[str] = None):
        super().__init__(f"SR {sr_type}", identifier)


class SRHeaderNotFoundException(SRNotFoundException):
    def __init__(self, identifier: Optional[str] = None):
        super().__init__("Headers", identifier)


class SRItemsNotFoundException(SRNotFoundException):
    def __init__(self, identifier: Optional[str] = None):
        super().__init__("Items", identifier)


class SRAttachmentNotFoundException(SRNotFoundException):
    def __init__(self, identifier: Optional[str] = None):
        super().__init__("Attachments", identifier)


# 409 - Conflict
class ConflictException(BaseCustomException):
    """For resource conflicts"""

    def __init__(self, message: str, resource: Optional[str] = None):
        code = f"{resource.upper()}_CONFLICT" if resource else "RESOURCE_CONFLICT"
        super().__init__(409, message, code)


# 500 - Internal Server Error
class InternalServerException(BaseCustomException):
    """For internal server errors"""

    def __init__(
        self,
        message: str = "Internal server error",
        code: str = "INTERNAL_ERROR",
        details: Optional[str] = None,
    ):
        super().__init__(500, message, code, details=details)


class DatabaseException(BaseCustomException):
    """For database-related errors"""

    def __init__(
        self, message: str = "Database operation failed", details: Optional[str] = None
    ):
        super().__init__(500, message, "DATABASE_ERROR", details=details)


# Utility functions
def get_request_info(request: Request) -> Dict[str, Any]:
    """Extract request information for logging and responses"""
    request_id = getattr(request.state, "request_id", None)
    if not request_id:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        logger.warning("Request ID was missing, generated fallback")

    return {
        "request_id": request_id,
        "path": request.url.path,
        "method": request.method,
        "client_ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
    }


def create_error_response(
    status_code: int,
    message: str,
    code: str,
    request_info: Dict[str, Any],
    details: Optional[str] = None,
    field: Optional[str] = None,
    include_stack_trace: bool = False,
    exception: Optional[Exception] = None,
) -> ErrorResponse:
    """Create standardized error response"""

    error_response = ErrorResponse(
        timestamp=datetime.now(timezone.utc),
        status_code=status_code,
        path=request_info["path"],
        message=message,
        code=code,
        details=details,
        field=field,
        request_id=request_info["request_id"],
        environment=settings.ENVIRONMENT if not settings.is_production() else None,
    )

    # Add stack trace based on settings and environment
    if include_stack_trace and settings.include_stack_trace:
        if exception:
            error_response.stack_trace = "".join(
                traceback.format_exception(
                    type(exception), exception, exception.__traceback__
                )
            )
        else:
            error_response.stack_trace = traceback.format_exc()

    return error_response


# Exception Handlers
async def base_custom_exception_handler(
    request: Request, exc: BaseCustomException
) -> JSONResponse:
    """Global exception handler for custom exceptions"""

    request_info = get_request_info(request)

    # Log the exception with appropriate level
    log_level = logging.ERROR if exc.status_code >= 500 else logging.WARNING
    logger.log(
        log_level,
        f"Exception: {exc.code} - {exc.message}",
        extra={
            "request_id": request_info["request_id"],
            "path": request_info["path"],
            "method": request_info["method"],
            "status_code": exc.status_code,
            "error_code": exc.code,
            "client_ip": request_info["client_ip"],
        },
    )

    error_response = create_error_response(
        status_code=exc.status_code,
        message=exc.message,
        code=exc.code,
        request_info=request_info,
        details=exc.details,
        field=exc.field,
        include_stack_trace=exc.status_code >= 500,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(mode="json", exclude_none=True),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handler for FastAPI validation errors"""

    request_info = get_request_info(request)

    # Format validation errors
    validation_errors = []
    for error in exc.errors():
        field = (
            ".".join(str(x) for x in error["loc"][1:])
            if len(error["loc"]) > 1
            else str(error["loc"][0])
        )
        validation_errors.append(
            ValidationErrorDetail(
                field=field,
                message=error["msg"],
                type=error["type"],
                input=(
                    error.get("input") if not settings.is_production() else None
                ),  # Hide input in production
            )
        )

    error_response = ValidationErrorResponse(
        timestamp=datetime.now(timezone.utc),
        path=request_info["path"],
        validation_errors=validation_errors,
        request_id=request_info["request_id"],
        environment=settings.ENVIRONMENT if not settings.is_production() else None,
    )

    logger.warning(
        f"Validation error: {len(validation_errors)} field(s) failed validation",
        extra={
            "request_id": request_info["request_id"],
            "path": request_info["path"],
            "method": request_info["method"],
            "validation_errors": [
                {"field": ve.field, "type": ve.type} for ve in validation_errors
            ],
            "client_ip": request_info["client_ip"],
        },
    )

    return JSONResponse(
        status_code=422,
        content=error_response.model_dump(mode="json", exclude_none=True),
    )


async def http_exception_handler_custom(
    request: Request, exc: HTTPException
) -> JSONResponse:
    """Handler for generic HTTP exceptions"""

    request_info = get_request_info(request)

    # Determine error code based on status code
    error_codes = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        422: "UNPROCESSABLE_ENTITY",
        500: "INTERNAL_SERVER_ERROR",
        502: "BAD_GATEWAY",
        503: "SERVICE_UNAVAILABLE",
    }

    error_code = error_codes.get(exc.status_code, f"HTTP_{exc.status_code}")

    error_response = create_error_response(
        status_code=exc.status_code,
        message=str(exc.detail),
        code=error_code,
        request_info=request_info,
    )

    log_level = logging.ERROR if exc.status_code >= 500 else logging.WARNING
    logger.log(
        log_level,
        f"HTTP Exception: {exc.status_code} - {exc.detail}",
        extra={
            "request_id": request_info["request_id"],
            "path": request_info["path"],
            "method": request_info["method"],
            "status_code": exc.status_code,
            "client_ip": request_info["client_ip"],
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(mode="json", exclude_none=True),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for any unhandled exceptions"""

    request_info = get_request_info(request)

    # Log the full exception for debugging
    logger.error(
        f"Unhandled exception: {type(exc).__name__}: {str(exc)}",
        exc_info=True,
        extra={
            "request_id": request_info["request_id"],
            "path": request_info["path"],
            "method": request_info["method"],
            "exception_type": type(exc).__name__,
            "client_ip": request_info["client_ip"],
        },
    )

    # Environment-specific error messages
    if settings.is_development():
        message = f"{type(exc).__name__}: {str(exc)}"
    elif settings.is_staging():
        message = "An error occurred while processing your request"
    else:  # production
        message = "An unexpected error occurred"

    error_response = create_error_response(
        status_code=500,
        message=message,
        code="INTERNAL_SERVER_ERROR",
        request_info=request_info,
        include_stack_trace=True,
        exception=exc,
    )

    return JSONResponse(
        status_code=500,
        content=error_response.model_dump(mode="json", exclude_none=True),
    )
