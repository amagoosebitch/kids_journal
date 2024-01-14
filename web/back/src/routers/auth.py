from pathlib import Path

import jwt
from fastapi import Depends, Request
from starlette import status
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates

from auth.settings import JWTSettings
from db.services.employee import EmployeeService
from dependencies import create_employee_service
from src.auth import (
    TelegramAuth,
    TelegramDataError,
    TelegramDataIsOutdated,
    TelegramLoginWidget,
    WidgetSize,
    validate_telegram_data,
)
from src.settings import BotConfig, load_bot_config

templates = Jinja2Templates(Path(__file__).parent.parent / "templates")


def _create_jwt_token(
    *,
    jwt_settings: JWTSettings,
    model_data: TelegramAuth,
    employee_service: EmployeeService,
) -> str | None:
    employee = employee_service.get_by_tg_user_id(str(model_data.id))
    if employee is None:
        return None
    token = jwt.encode(
        {"user_id": employee.telegram_id, "role": employee.role},
        jwt_settings.secret_key,
        algorithm=jwt_settings.algorithm,
    )
    return token


def _get_json_response(jwt_token: str | None) -> JSONResponse:
    if jwt_token is None:
        return JSONResponse(
            content={"message": "Auth failed, no access"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    response = JSONResponse(content={"message": "Auth success"})
    response.set_cookie(key="token", value=jwt_token)
    return response


def get_telegram_redirect_widget(request: Request, telegram_login: str):
    login_widget = TelegramLoginWidget(
        telegram_login=telegram_login,
        size=WidgetSize.LARGE,
        user_photo=False,
        corner_radius=0,
    )

    redirect_url = str(request.url_for("login"))
    return login_widget.redirect_telegram_login_widget(redirect_url=redirect_url)


async def login(
    request: Request,
    query_params: TelegramAuth = Depends(TelegramAuth),
    config: BotConfig = Depends(load_bot_config),
    jwt_settings: JWTSettings = Depends(JWTSettings),
    employee_service: EmployeeService = Depends(create_employee_service),
):
    telegram_token = config.telegram_token
    telegram_login = config.telegram_login
    redirect_widget = get_telegram_redirect_widget(
        request=request, telegram_login=telegram_login
    )

    if not query_params.model_dump().get("hash"):
        return templates.TemplateResponse(
            "login.html",
            context={
                "request": request,
                "redirect_telegram_login_widget": redirect_widget,
            },
        )

    try:
        validated_data = validate_telegram_data(telegram_token, query_params)
        if not validated_data:
            return
        token = _create_jwt_token(
            jwt_settings=jwt_settings,
            model_data=query_params,
            employee_service=employee_service,
        )
        return _get_json_response(token)
    except TelegramDataIsOutdated:
        return HTMLResponse(
            "The authentication data is expired.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except TelegramDataError:
        return HTMLResponse(
            "The request contains invalid data.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
