from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from starlette.responses import HTMLResponse, RedirectResponse, Response
from starlette.templating import Jinja2Templates

from auth import (
    TelegramAuth,
    TelegramDataError,
    TelegramDataIsOutdated,
    TelegramLoginWidget,
    WidgetSize,
    validate_telegram_data,
)
from db.services.groups import GroupModel
from db.services.organization import OrganizationModel
from dependencies import create_group_service, create_organization_service
from settings import BotConfig, load_bot_config

router = APIRouter()

templates = Jinja2Templates(Path(__file__).parent / "templates")


def create_jwt_token():
    # потом
    pass


def set_cookies():
    # возможно потом
    pass


@router.get("/", name="index")
async def index(request: Request):
    """
    Index page just redirects to login page.
    """
    return RedirectResponse(url=request.url_for("login"))


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


@router.post("/organizations", status_code=201)
async def create_organization(
    organization: OrganizationModel,
    organization_service=Depends(create_organization_service),
):
    response = organization_service.create_organization(organization)

    return {
        "organization_id": response.organization_id
    }  # посмотреть че возвращает запрос


@router.get("/organizations")
async def get_organizations(
    organization_service=Depends(create_organization_service),
):
    response = organization_service.get_all()

    return response  # посмотреть че возвращает запрос


@router.get("/organizations/{organization_id}")
async def get_organization(
    organization_id: UUID,
    organization_service=Depends(create_organization_service),
):
    response = organization_service.get_by_id(organization_id)

    if not response:
        return Response("Organization not found", status_code=404)

    return Response(response.json(), status_code=200)


@router.post("/groups", status_code=201)
async def add_group_to_organization(
    group: GroupModel,
    group_service=Depends(create_group_service),
):
    response = group_service.create_group(group)

    return {"group_id": response.group_id}


@router.get("/organizations/{organizationId}/groups")
async def get_groups_by_organization(
    organization_id: UUID,
    group_service=Depends(create_group_service),
):
    response = group_service.get_all_for_organization(organization_id)
    #  проверить что если нет такой организации с чем упадем и заэксептить и вернуть 404
    return Response(response.json(), status_code=200)


@router.get("groups/{groupId}")
async def get_group(
    group_id: UUID,
    group_service=Depends(create_group_service),
):
    response = group_service.get_by_id(group_id)
    #  проверить что если нет такой организации с чем упадем и заэксептить и вернуть 404
    if not response:
        return Response("Group not found", status_code=404)

    return Response(response.json(), status_code=200)
