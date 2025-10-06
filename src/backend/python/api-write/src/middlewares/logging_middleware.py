from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from core.logger import logger
import time

middleware_logger = logger.getChild("middleware")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        middleware_logger.info(f"START {request.method} {request.url}")
        response = await call_next(request)
        duration = (time.time() - start) * 1000
        middleware_logger.info(f"END {request.method} {request.url} - status {response.status_code} ({duration:.2f}ms)")
        return response