from fastapi import Depends, Request
from starlette import status
from starlette.responses import HTMLResponse

from src.auth import (
    TelegramAuth,
    TelegramDataError,
    TelegramDataIsOutdated,
    TelegramLoginWidget,
    WidgetSize,
    validate_telegram_data,
)
from src.routers.routers import router, templates
from src.routers.utils import create_jwt_token, set_cookies
from src.settings import BotConfig, load_bot_config


@router.get("/login", name="login")
async def login(
    request: Request,
    query_params: TelegramAuth = Depends(TelegramAuth),
    config: BotConfig = Depends(load_bot_config),
):
    telegram_token = config.telegram_token
    telegram_login = config.telegram_login

    login_widget = TelegramLoginWidget(
        telegram_login=telegram_login,
        size=WidgetSize.LARGE,
        user_photo=False,
        corner_radius=0,
    )

    redirect_url = str(request.url_for("login"))
    redirect_widget = login_widget.redirect_telegram_login_widget(
        redirect_url=redirect_url
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

        create_jwt_token()
        set_cookies()
        return templates.TemplateResponse(
            "profile.html", context={"request": request, **validated_data}
        )
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
