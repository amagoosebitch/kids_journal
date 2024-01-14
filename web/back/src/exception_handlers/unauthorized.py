from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse


async def handle_auth_error(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return RedirectResponse(url="/error")
    return JSONResponse({"message": str(exc)})
