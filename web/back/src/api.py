from http.client import HTTPException

import uvicorn
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.presentation import (
    delete_presentation,
    get_all_presentations_for_subject,
    get_presentation,
    upsert_presentation,
)
from routers.schedule import (
    delete_lesson,
    get_schedule_for_child_by_date,
    get_schedule_for_group,
    unlink_lesson_from_child,
    upsert_lesson,
)
from routers.subject import (
    create_subject,
    delete_subject,
    get_all_subjects_for_organization,
    get_subject,
)
from src.exception_handlers.unauthorized import handle_auth_error
from src.routers.auth import login
from src.routers.child import delete_child, upsert_child
from src.routers.employee import (
    delete_employee,
    get_employees_for_organization,
    get_employees_organization_names_by_phone,
    get_groups_for_employee,
    get_user_by_phone,
    get_user_by_tg_id,
    link_employee_to_group,
    unlink_group_from_employee,
    upsert_employee,
)
from src.routers.groups import (  # add_children_to_group,
    add_group_to_organization,
    delete_group,
    get_children_by_group_id,
    get_group,
    get_groups_by_organization,
)
from src.routers.organization import (
    create_organization,
    delete_organization,
    get_organization,
    get_organizations,
    get_organizations_for_user_by_phone,
)
from src.routers.parent import (
    create_parent,
    delete_parent,
    get_parent_by_tg_id,
    get_parents_by_child_id,
)
from src.routers.skills import (
    delete_skill_level,
    get_all_skill_levels,
    get_all_skills_for_child,
    get_skill_level_by_id,
    upsert_skill_for_child,
    upsert_skill_level,
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
    router.add_api_route("/groups_/{group_id}", delete_group, methods=["DELETE"])
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
    router.add_api_route(
        "/organization/{organization_id}", delete_organization, methods=["DELETE"]
    )

    # Auth
    router.add_api_route("/login", login, methods=["GET"])

    # Parent
    router.add_api_route("/parents", create_parent, methods=["POST"])
    router.add_api_route("/parents/{tg_id}", get_parent_by_tg_id, methods=["GET"])
    router.add_api_route(
        "/parents/child/{child_id}", get_parents_by_child_id, methods=["GET"]
    )
    router.add_api_route("/parent/{parent_id}", delete_parent, methods=["DELETE"])

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
    router.add_api_route(
        "/employees/{employee_id}/groups", get_groups_for_employee, methods=["GET"]
    )
    router.add_api_route(
        "/employees/{employee_id}/groups/{group_id}",
        link_employee_to_group,
        methods=["POST"],
    )
    router.add_api_route(
        "/employees/{employee_id}/groups/{group_id}",
        unlink_group_from_employee,
        methods=["DELETE"],
    )
    router.add_api_route(
        "/employees/{employee_id}", delete_employee, methods=["DELETE"]
    )

    # Child
    router.add_api_route("/{group_id}/child", upsert_child, methods=["POST"])
    router.add_api_route("/{group_id}/child", get_children_by_group_id, methods=["GET"])
    router.add_api_route(
        "/children/{child_id}/skills/{presentation_id}/",
        upsert_skill_for_child,
        methods=["POST"],
    )
    router.add_api_route(
        "/children/{child_id}/skills/", get_all_skills_for_child, methods=["GET"]
    )
    router.add_api_route("/children/{child_id}", delete_child, methods=["DELETE"])

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
    router.add_api_route("/subjects/{subject_id}", delete_subject, methods=["DELETE"])

    # Presentation
    router.add_api_route(
        "/subjects/{subject_id}/presentations", upsert_presentation, methods=["POST"]
    )
    router.add_api_route(
        "/subjects/{subject_id}/presentations",
        get_all_presentations_for_subject,
        methods=["GET"],
    )
    router.add_api_route(
        "/organizations/{organization_id}/subjects/{subject_id}/{presentation_id}",
        get_presentation,
        methods=["GET"],
    )
    router.add_api_route(
        "/presentations/{presentation_id}", delete_presentation, methods=["DELETE"]
    )

    # Schedule
    router.add_api_route("/lessons", upsert_lesson, methods=["POST"])
    router.add_api_route("/lessons/{group_id}", get_schedule_for_group, methods=["GET"])
    router.add_api_route(
        "/lessons/individual/{child_id}",
        get_schedule_for_child_by_date,
        methods=["GET"],
    )
    router.add_api_route(
        "/lessons/individual/{child_id}", unlink_lesson_from_child, methods=["DELETE"]
    )
    router.add_api_route("/lessons/{lesson_id}", delete_lesson, methods=["DELETE"])

    # Skills
    router.add_api_route("/skills_levels", upsert_skill_level, methods=["POST"])
    router.add_api_route("/skills_levels", get_all_skill_levels, methods=["GET"])
    router.add_api_route(
        "/skills_levels/{skill_level_id}", get_skill_level_by_id, methods=["GET"]
    )
    router.add_api_route(
        "/skills_levels/{skill_level_id}", delete_skill_level, methods=["DELETE"]
    )

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
