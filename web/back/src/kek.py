import os
import uuid
from datetime import datetime, timedelta
from uuid import UUID

from db.settings import YDBSettings
from dependencies import (
    create_child_service,
    create_employee_service,
    create_group_service,
    create_organization_service,
    create_parent_service,
    create_pool,
    create_schedule_service,
    create_subject_service,
)
from models.child import ChildModel
from models.employees import EmployeeModel
from models.entity import Gender
from models.groups import GroupModel
from models.organizations import OrganizationModel
from models.parents import ParentModel
from models.schedule import ScheduleModel
from models.subjects import SubjectModel
from routers.employee import create_employee
from routers.subject import create_subject

os.environ["YDB_ENDPOINT"] = "grpcs://ydb.serverless.yandexcloud.net:2135"
os.environ["YDB_DATABASE"] = "/ru-central1/b1ge6sseudpphs9ug20c/etnq6fuuhe9nttldc4vh"
os.environ[
    "YDB_ACCESS_TOKEN_CREDENTIALS"
] = "t1.9euelZrKlMiMypLLnM7OmovJms7OzO3rnpWazpnIz8fGlo-UmcuZkZfIz4nl8_cOO2ZS-e8tYCUp_N3z905pY1L57y1gJSn8zef1656VmpeOm8aRi4uOlIrLiY7Py5LI7_zF656VmpeOm8aRi4uOlIrLiY7Py5LI.xUdNmPHJnVsI6MtAaT8bPPdKlgF5Xfz6HfxGQLfaSp3rsT0Vzq2qEpzUyP6GEMYLqcgRWAkfT0yNFqtAFtKxBg"

settings = YDBSettings()
pool = create_pool(settings)

group_service = create_group_service(pool, settings)
child_service = create_child_service(pool, settings)
parent_service = create_parent_service(pool, settings)
subject_service = create_subject_service(pool, settings)
schedule = create_schedule_service(pool, settings)
employee_service = create_employee_service(pool, settings)
# child = ChildModel(name="ребенок_2", first_name="Иван", last_name="Иванов", birth_date=datetime.now(), gender=Gender.FEMALE)
# parent_service.create_parent(parent)
# child_service.link_to_group("fb551f8d-14f3-4e74-8fc9-99aaaf433f9e", "3120cdcd-602d-4b17-b0a3-96b657ef8c39")
# print(parent_service.get_by_tg_user_id("dattebayob"))
# print(group_service.get_all())
# print(group_service.get_all_for_organization())
# print(group_service.get_by_id(group.group_id))
# print(organization_service.get_by_name("марк"))
# print(organization_service.get_by_id(UUID('8d413fc2-3411-41be-a701-862ec74d352b')))

# schedule_service = create_schedule_service(pool, settings)


# subject_1 = SubjectModel(name='матеша')
# subject_2 = SubjectModel(name='физра')
child_ids = ["3120cdcd-602d-4b17-b0a3-96b657ef8c39"]
data1 = ScheduleModel(
    group_id="fb551f8d-14f3-4e74-8fc9-99aaaf433f9e",
    teacher_id="0c304973-f531-4296-888b-48e78c2e1306",
    subject_id="2f044cb8-e671-4fac-9f47-78266fafe49b",
    presentation_id=uuid.uuid4(),
    start_lesson=datetime.today(),
    end_lesson=datetime.today() + timedelta(hours=1),
)
data2 = ScheduleModel(
    group_id="fb551f8d-14f3-4e74-8fc9-99aaaf433f9e",
    teacher_id="0c304973-f531-4296-888b-48e78c2e1306",
    subject_id="4c666b25-524c-4fc9-98ce-23b9d9d8ab20",
    presentation_id=uuid.uuid4(),
    start_lesson=datetime.today(),
    end_lesson=datetime.today() + timedelta(hours=2),
    child_ids=child_ids,
)
# schedule.create_schedule(data1)
# schedule.create_schedule(data2)
# schedule.create_child_schedule_pairs(str(data2.schedule_id), child_ids)
# print(data1.end_lesson)

# create_subject("8d413fc2-3411-41be-a701-862ec74d352b", subject_1, group_service, subject_service)
# create_subject("8d413fc2-3411-41be-a701-862ec74d352b", subject_2, group_service, subject_service)
# print(subject_service.get_all_for_organization())
employee = EmployeeModel(
    name="employee", first_name="kek", gender="MALE", role_id="Воспитатель"
)
# create_employee(employee, '8d413fc2-3411-41be-a701-862ec74d352b', organization_service=create_employee_service(pool, settings), groups_service=group_service)

lst = schedule.get_for_children_by_time(
    "fb551f8d-14f3-4e74-8fc9-99aaaf433f9e", datetime.now()
)
lst2 = schedule.get_for_group_by_time(
    "fb551f8d-14f3-4e74-8fc9-99aaaf433f9e", datetime.now()
)
