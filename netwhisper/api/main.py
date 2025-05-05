"""
Main entry point for the FastAPI application.

uvicorn netwhisper.api.main:app --reload --log-config logging_config.json
"""

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from netwhisper.api.middleware.logger import LogRawBodyMiddleware
from netwhisper.api.routes import device, inventory
from netwhisper.device import DeviceServiceError
from netwhisper.logger import logger

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request, exc):
    logger.error("Request validation error", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.exception_handler(DeviceServiceError)
async def http_exception_handler(request, exc):
    logger.error("Device service error", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"status": "error", "message": str(exc)},
    )


app.add_middleware(LogRawBodyMiddleware)

app.include_router(device.router, prefix="/device")
app.include_router(inventory.router, prefix="/inventory")


@app.get("/")
def root():
    return {"status": "NetWhisper API is running"}
