from pathlib import Path

import jwt
from fastapi import Depends, Request
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from auth.settings import JWTSettings, create_redirect_settings, RedirectSettings
from db.services.employee import EmployeeService
from dependencies import create_employee_service, jwt_settings
from models.employees import EmployeeModel
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
    employee: EmployeeModel | None,
) -> str | None:
    if employee is None:
        return None
    token = jwt.encode(
        {"user_id": employee.tg_user_id, "role": employee.role_id.name, "phone_number": employee.phone_number},
        jwt_settings.secret_key,
        algorithm=jwt_settings.algorithm,
    )
    return token


def _get_redirect_response(jwt_token: str | None, redirect_settings: RedirectSettings) -> RedirectResponse:
    if jwt_token is None:
        return RedirectResponse(url=redirect_settings.url, status_code=status.HTTP_304_NOT_MODIFIED)
    response = RedirectResponse(url=redirect_settings.main_url + f'?cookie={jwt_token}', status_code=status.HTTP_302_FOUND)
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
    jwt_settings: JWTSettings = Depends(jwt_settings),
    employee_service: EmployeeService = Depends(create_employee_service),
    redirect_settings: RedirectSettings = Depends(create_redirect_settings),
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
        employee = employee_service.get_by_tg_user_id(str(query_params.id))
        token = _create_jwt_token(
            jwt_settings=jwt_settings,
            employee=employee,
        )
        return _get_redirect_response(token, redirect_settings)
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
