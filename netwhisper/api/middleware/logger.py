from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from netwhisper.logger import logger


class LogRawBodyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Read the raw body
        body = await request.body()
        logger.info(f"Raw request body: {body.decode('utf-8')}")

        # Recreate request stream for downstream use
        async def receive():
            return {"type": "http.request", "body": body}

        request._receive = receive

        response = await call_next(request)
        return response
