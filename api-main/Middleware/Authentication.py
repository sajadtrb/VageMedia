from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print('Authentication Worked')
        response = await call_next(request)
        return response