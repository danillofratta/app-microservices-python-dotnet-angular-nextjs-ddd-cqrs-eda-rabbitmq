from fastapi.responses import JSONResponse
from fastapi import Request
from core.logger import logger
from domain.exceptions import DomainError

async def handler(request: Request, exc: Exception):
    logger.exception(exc)
    if isinstance(exc, DomainError):
        return JSONResponse({"detail": str(exc)}, status_code=400)
    return JSONResponse({"detail": "Internal server error"}, status_code=500)
