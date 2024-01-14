from fastapi import HTTPException
from starlette.requests import Request


def get_auth_user(request: Request):
    jwt_token = request.cookies.get("Authorization")
    if not jwt_token:
        raise HTTPException(status_code=401)
    return True