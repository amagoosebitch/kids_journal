from http.client import HTTPException

import uvicorn
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.presentation import create_presentation, get_presentation
from routers.schedule import create_lesson, get_schedule_for_group
from routers.subject import (
    create_subject,
    get_all_subjects_for_organization,
    get_subject,
)
from src.exception_handlers.unauthorized import handle_auth_error
from src.routers.auth import login
from src.routers.child import create_child
from src.routers.employee import create_employee, get_employee_by_tg_id, get_employees_for_organization
from src.routers.groups import (
    add_children_to_group,
    add_group_to_organization,
    get_children_by_group_id,
    get_group,
    get_groups_by_organization,
)
from src.routers.organization import (
    create_organization,
    get_organization,
    get_organizations,
)
from src.routers.parent import (
    create_parent,
    get_parent_by_tg_id,
    get_parents_by_child_id,
)
from src.routers.user import try_merge_user_by_phone
from src.settings import load_api_settings


def init_app() -> FastAPI:
    app = FastAPI(debug=True)
    router = APIRouter()

    # Groups
    router.add_api_route("/groups", add_group_to_organization, methods=["POST"])
    router.add_api_route(
        "/organizations/{organization_id}/groups",
        get_groups_by_organization,
        methods=["GET"],
    )
    router.add_api_route("/groups/{group_id}", get_group, methods=["GET"])
    router.add_api_route(
        "/groups/link_children", add_children_to_group, methods=["POST"]
    )

    # Organizations
    router.add_api_route("/organizations", create_organization, methods=["POST"])
    router.add_api_route("/organizations", get_organizations, methods=["GET"])
    router.add_api_route(
        "/organizations/{organization_id}", get_organization, methods=["GET"]
    )

    # Auth
    router.add_api_route("/login", login, methods=["GET"])

    # Parent
    router.add_api_route("/parents", create_parent, methods=["POST"])
    router.add_api_route("/parents/{tg_id}", get_parent_by_tg_id, methods=["GET"])
    router.add_api_route(
        "/parents/child/{child_id}", get_parents_by_child_id, methods=["GET"]
    )

    # Employee
    router.add_api_route(
        "/organizations/{organization_id}/employee", create_employee, methods=["POST"]
    )
    router.add_api_route(
        "/organizations/{organization_id}/employee", get_employees_for_organization, methods=["GET"]
    )
    router.add_api_route("/employee/{tg_id}", get_employee_by_tg_id, methods=["GET"])

    # Child
    router.add_api_route("/{group_id}/child", create_child, methods=["POST"])
    router.add_api_route("/{group_id}/child", get_children_by_group_id, methods=["GET"])

    # User
    router.add_api_route("/user_merge", try_merge_user_by_phone, methods=["POST"])

    # Subject
    router.add_api_route(
        "/organizations/{organization_id}/subjects/{subject_id}",
        get_subject,
        methods=["GET"],
    )
    router.add_api_route(
        "/organizations/{organization_id}/subjects",
        get_all_subjects_for_organization,
        methods=["GET"],
    )
    router.add_api_route(
        "/organizations/{organization_id}/subjects", create_subject, methods=["POST"]
    )

    # Presentation
    router.add_api_route(
        "/subjects/{subject_id}/presentations", create_presentation, methods=["POST"]
    )
    router.add_api_route(
        "/organizations/{organizationId}/subjects/{subjectId}/{presentationId}",
        get_presentation,
        methods=["GET"],
    )

    # Schedule
    router.add_api_route("/lessons", create_lesson, methods=["POST"])
    router.add_api_route("/lessons/{group_id}", get_schedule_for_group, methods=["GET"])

    api_settings = load_api_settings()

    # Midddlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_settings.allow_origins,
        allow_credentials=api_settings.allow_credentials,
        allow_methods=api_settings.allow_methods,
        allow_headers=api_settings.allow_headers,
    )

    # Exception handlers
    app.add_exception_handler(HTTPException, handle_auth_error)

    app.include_router(router)
    return app


if __name__ == "__main__":
    import os

    os.environ["YDB_ENDPOINT"] = "grpcs://ydb.serverless.yandexcloud.net:2135"
    os.environ["YDB_DATABASE"] = "/ru-central1/b1ge6sseudpphs9ug20c/etnq6fuuhe9nttldc4vh"
    os.environ[
        "YDB_ACCESS_TOKEN_CREDENTIALS"
    ] = "t1.9euelZqPm52JxpuQjIycy8iPxsqZne3rnpWazpnIz8fGlo-UmcuZkZfIz4nl8_cVWGRS-e8ZEhxH_d3z91UGYlL57xkSHEf9zef1656VmpqPkZWUkIvKyc6PyZybnsrJ7_zF656VmpqPkZWUkIvKyc6PyZybnsrJ.VCuzEhy6Ehk0pENz3W5zMBsKK4yEgFLTpaEZjmHd9DIGNFWyyWrKECTbjHsg_VPkimm-3Ngzp4cTx7xQIUAXBQ"
    os.environ["AUTH_TELEGRAM_TOKEN"] = "6371723269:AAHI3cGJzUOj9HI0CyPW4cA2-1o9Pt5nis0"
    os.environ['AUTH_TELEGRAM_LOGIN'] = 'kind_world_bot'
    os.environ['JWT_SECRET_KEY'] = 'b794385f2d1ef7ab4d9273d1906381b44f2f6f2588a3efb96a49188331984753'

    uvicorn.run(init_app, host="0.0.0.0", port=8080)
