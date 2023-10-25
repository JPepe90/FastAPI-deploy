from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from typing import Optional

class ErrorHandler(BaseHTTPMiddleware):
  def __init__(self, app: FastAPI) -> None:
    super().__init__(app)
  
  async def dispatch(self, request: Request, call_next) -> Response or JSONResponse:
    try:
      return await call_next(request)
    except Exception as e:
      error = {
        'error': str(e)
      }
      return JSONResponse(status_code=500, content=error)