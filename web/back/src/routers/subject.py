from fastapi import Depends

from db.services.groups import GroupService
from db.services.subjects import SubjectService
from models.subjects import SubjectModel
from src.dependencies import create_group_service, create_subject_service


async def create_subject(
    organization_id: str,
    subject: SubjectModel,
    groups_service: GroupService = Depends(create_group_service),
    subject_service: SubjectService = Depends(create_subject_service),
) -> None:
    subject_service.create_subject(subject)
    group_ids = [
        str(group.group_id)
        for group in groups_service.get_all_for_organization(organization_id)
    ]
    if group_ids:
        subject_service.create_group_subject_pair(group_ids, str(subject.subject_id))


async def get_subject(
    organization_id: str,
    subject_id: str,
    subject_service: SubjectService = Depends(create_subject_service),
) -> SubjectModel:
    return subject_service.get_by_id(subject_id)


async def get_all_subjects_for_organization(
    organization_id: str = None,
    subject_service: SubjectService = Depends(create_subject_service),
) -> list[SubjectModel]:
    return subject_service.get_all()


async def delete_subject(
    subject_id: str, subject_service: SubjectService = Depends(create_subject_service)
) -> None:
    return subject_service.delete_by_id(subject_id=subject_id)
