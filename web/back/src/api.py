import uvicorn
from fastapi import APIRouter, FastAPI

from src.routers.auth import login
from src.routers.groups import (
    add_group_to_organization,
    get_group,
    get_groups_by_organization,
)
from src.routers.index import index
from src.routers.organization import (
    create_organization,
    get_organization,
    get_organizations,
)


def init_app() -> FastAPI:
    app = FastAPI(debug=True)
    router = APIRouter()

    # Groups
    router.add_api_route("/groups", add_group_to_organization, methods=["POST"])
    router.add_api_route(
        "/organizations/{organizationId}/groups",
        get_groups_by_organization,
        methods=["GET"],
    )
    router.add_api_route("/groups/{groupId}", get_group, methods=["GET"])

    # Organizations
    router.add_api_route("/organizations", create_organization, methods=["POST"])
    router.add_api_route("/organizations", get_organizations, methods=["GET"])
    router.add_api_route(
        "/organizations/{organization_id}", get_organization, methods=["GET"]
    )

    # Auth
    router.add_api_route("/login", login, methods=["GET"])
    router.add_api_route("/", index, methods=["GET"])

    app.include_router(router)
    return app


if __name__ == "__main__":
    uvicorn.run(init_app, port=8000)
