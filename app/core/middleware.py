# app/core/middleware.py
import uuid
import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add request ID to all requests"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Process request
        response = await call_next(request)

        # Add request ID to headers for client reference
        response.headers["X-Request-ID"] = request_id

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Enhanced logging middleware with environment-specific behavior"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = getattr(request.state, "request_id", "unknown")

        # Skip logging for health checks in production to reduce noise
        should_log_request = True
        if settings.is_production() and request.url.path in [
            "/health",
            "/",
            "/favicon.ico",
        ]:
            should_log_request = False

        # Log request start
        if should_log_request:
            log_extra = {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host if request.client else None,
            }

            # Add more details in development
            if settings.is_development():
                log_extra.update(
                    {
                        "query_params": (
                            str(request.query_params) if request.query_params else None
                        ),
                        "user_agent": request.headers.get("user-agent"),
                        "content_type": request.headers.get("content-type"),
                    }
                )

            logger.info(
                f"Request started: {request.method} {request.url.path}", extra=log_extra
            )

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        if should_log_request:
            log_level = logging.WARNING if response.status_code >= 400 else logging.INFO

            log_extra = {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": round(process_time, 4),
                "client_ip": request.client.host if request.client else None,
            }

            # Add response details in development
            if settings.is_development():
                log_extra.update(
                    {
                        "content_length": response.headers.get("content-length"),
                        "content_type": response.headers.get("content-type"),
                    }
                )

            logger.log(
                log_level,
                f"Request completed: {request.method} {request.url.path} - {response.status_code}",
                extra=log_extra,
            )

        # Add processing time to response headers
        response.headers["X-Process-Time"] = str(round(process_time, 4))

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers based on environment"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Basic security headers for all environments
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Production-specific security headers
        if settings.is_production():
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
            response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response
