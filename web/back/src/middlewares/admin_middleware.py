import jwt
from fastapi import HTTPException
from starlette.requests import Request

from auth.settings import JWTSettings


def get_auth_user(request: Request, jwt_settings: JWTSettings):
    jwt_token = request.cookies.get("Authorization")
    if not jwt_token:
        raise HTTPException(status_code=401)
    role = jwt.decode(jwt_token, jwt_settings.secret_key, algorithms=[jwt_settings.algorithm])["role"]
    if role != "admin":
        raise HTTPException(status_code=401)
    return True