"""
Logging and error handling middleware.
You probably don't need to touch this.
"""

import time
import logging
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import FastAPI

logger = logging.getLogger("api")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = (time.time() - start) * 1000

        log_data = {
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": round(duration, 2),
        }
        logger.info(json.dumps(log_data))
        response.headers["X-Process-Time-Ms"] = str(round(duration, 2))
        return response


def add_logging_middleware(app: FastAPI):
    logging.basicConfig(level=logging.INFO)
    app.add_middleware(LoggingMiddleware)
