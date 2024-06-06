from http.client import HTTPException

import uvicorn
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.presentation import (
    create_presentation,
    get_presentation,
    get_all_presentations_for_subject,
)
from routers.schedule import upsert_lesson, get_schedule_for_group, get_schedule_for_child_by_date, unlink_lesson_from_child
from routers.subject import (
    create_subject,
    get_all_subjects_for_organization,
    get_subject,
)
from src.exception_handlers.unauthorized import handle_auth_error
from src.routers.auth import login
from src.routers.child import upsert_child
from src.routers.employee import (
    upsert_employee,
    get_employees_for_organization,
    get_employees_organization_names_by_phone,
    get_user_by_phone,
    get_user_by_tg_id,
    link_employee_to_group, unlink_group_from_employee, get_groups_for_employee
)
from src.routers.groups import (  # add_children_to_group,
    add_group_to_organization,
    get_children_by_group_id,
    get_group,
    get_groups_by_organization,
)
from src.routers.organization import (
    create_organization,
    get_organization,
    get_organizations,
    get_organizations_for_user_by_phone,
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
    # router.add_api_route(
    #     "/groups/link_children", add_children_to_group, methods=["POST"]
    # )

    # Organizations
    router.add_api_route("/organizations", create_organization, methods=["POST"])
    router.add_api_route("/organizations", get_organizations, methods=["GET"])
    router.add_api_route(
        "/organizations/phone/{phone_number}",
        get_organizations_for_user_by_phone,
        methods=["GET"],
    )
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
        "/organizations/{organization_id}/employee", upsert_employee, methods=["POST"]
    )
    router.add_api_route(
        "/organizations/{organization_id}/employee",
        get_employees_for_organization,
        methods=["GET"],
    )
    router.add_api_route("/employee/{tg_id}", get_user_by_tg_id, methods=["GET"])
    router.add_api_route("/employee/phone/{phone}", get_user_by_phone, methods=["GET"])
    router.add_api_route(
        "/employee/{phone}/organizations",
        get_employees_organization_names_by_phone,
        methods=["GET"],
    )
    router.add_api_route("/employees/{employee_id}/groups", get_groups_for_employee, methods=["GET"])
    router.add_api_route("/employees/{employee_id}/groups/{group_id}", link_employee_to_group, methods=["POST"])
    router.add_api_route("/employees/{employee_id}/groups/{group_id}", unlink_group_from_employee, methods=["DELETE"])

    # Child
    router.add_api_route("/{group_id}/child", upsert_child, methods=["POST"])
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
        "/subjects/{subject_id}/presentations", get_all_presentations_for_subject, methods=["GET"]
    )
    router.add_api_route(
        "/organizations/{organization_id}/subjects/{subject_id}/{presentation_id}",
        get_presentation,
        methods=["GET"],
    )

    # Schedule
    router.add_api_route("/lessons", upsert_lesson, methods=["POST"])
    router.add_api_route("/lessons/{group_id}", get_schedule_for_group, methods=["GET"])
    router.add_api_route("/lessons/individual/{child_id}", get_schedule_for_child_by_date, methods=["GET"])
    router.add_api_route("/lessons/individual/{child_id}", unlink_lesson_from_child, methods=["DELETE"])

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
    app.openapi_version = "3.0.0"
    return app


if __name__ == "__main__":
    uvicorn.run(init_app, host="0.0.0.0", port=8080)
