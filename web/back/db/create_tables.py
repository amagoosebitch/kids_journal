import argparse
import logging
from pathlib import Path
from typing import Any

import ydb


def create_tables(session_pool: Any, path: Path):
    def callee(session: Any):
        # organization
        session.create_table(
            str(path / "organization"),
            ydb.TableDescription()
            .with_primary_keys("organization_id")
            .with_columns(
                ydb.Column("organization_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("description", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("photo_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column(
                    "start_education_time", ydb.OptionalType(ydb.PrimitiveType.Datetime)
                ),
                ydb.Column(
                    "end_education_time", ydb.OptionalType(ydb.PrimitiveType.Datetime)
                ),
                ydb.Column(
                    "registration_date", ydb.OptionalType(ydb.PrimitiveType.Timestamp)
                ),
                ydb.Column(
                    "updated_date", ydb.OptionalType(ydb.PrimitiveType.Timestamp)
                ),
            ),
        )

        # group
        session.create_table(
            str(path / "group"),
            ydb.TableDescription()
            .with_primary_keys("group_id")
            .with_columns(
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("organization_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("age_range", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            )
            .with_indexes(
                ydb.TableIndex("organization_index").with_index_columns(
                    "organization_id"
                )
            ),
        )

        # group_teacher
        session.create_table(
            str(path / "group_teacher"),
            ydb.TableDescription()
            .with_primary_keys("group_id", "teacher_id")  # точно оба форяки ?
            .with_columns(
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("teacher_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # group_child
        session.create_table(
            str(path / "group_child"),
            ydb.TableDescription()
            .with_primary_keys("group_id", "child_id")  # точно оба форяки ?
            .with_columns(
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("child_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # group_subject
        session.create_table(
            str(path / "group_subject"),
            ydb.TableDescription()
            .with_primary_keys("group_id", "subject_id")  # точно оба форяки ?
            .with_columns(
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("subject_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # child
        session.create_table(
            str(path / "child"),
            ydb.TableDescription()
            .with_primary_keys("child_id")
            .with_columns(
                ydb.Column("child_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("first_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("last_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("birth_date", ydb.OptionalType(ydb.PrimitiveType.Datetime)),
                ydb.Column(
                    "start_education_date", ydb.OptionalType(ydb.PrimitiveType.Datetime)
                ),
                ydb.Column(
                    "start_education_time",
                    ydb.OptionalType(ydb.PrimitiveType.Timestamp),
                ),
                ydb.Column(
                    "end_education_time", ydb.OptionalType(ydb.PrimitiveType.Timestamp)
                ),
                ydb.Column("gender", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("parent_1_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("parent_2_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            ),
        )

        # child_schedule
        session.create_table(
            str(path / "child_schedule"),
            ydb.TableDescription()
            .with_primary_keys("child_id", "schedule_id")  # точно оба форяки ?
            .with_columns(
                ydb.Column("child_id", ydb.PrimitiveType.Utf8),
                ydb.Column("schedule_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # schedule
        session.create_table(
            str(path / "schedule"),
            ydb.TableDescription()
            .with_primary_keys("schedule_id")
            .with_columns(
                ydb.Column("schedule_id", ydb.PrimitiveType.Utf8),
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("start_lesson", ydb.OptionalType(ydb.PrimitiveType.Datetime)),
                ydb.Column("end_lesson", ydb.OptionalType(ydb.PrimitiveType.Datetime)),
                ydb.Column("description", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("teacher_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("subject_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("presentation_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("note_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("canceled", ydb.OptionalType(ydb.PrimitiveType.Bool)),
            )
            .with_indexes(
                ydb.TableIndex("teacher_index").with_index_columns("teacher_id"),
                ydb.TableIndex("subject_index").with_index_columns("subject_id"),
            ),
        )

        # note
        session.create_table(
            str(path / "note"),
            ydb.TableDescription()
            .with_primary_keys("note_id")
            .with_columns(
                ydb.Column("note_id", ydb.PrimitiveType.Utf8),
                ydb.Column("schedule_id", ydb.PrimitiveType.Utf8),
                ydb.Column("text", ydb.PrimitiveType.Utf8),
            ),
        )

        # subject
        session.create_table(
            str(path / "subject"),
            ydb.TableDescription()
            .with_primary_keys("subject_id")
            .with_columns(
                ydb.Column("subject_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("description", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("age_range", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            ),
        )

        # child_skills
        session.create_table(
            str(path / "child_skills"),
            ydb.TableDescription()
            .with_primary_keys("child_id", "skill_id")
            .with_columns(
                ydb.Column("child_id", ydb.PrimitiveType.Utf8),
                ydb.Column("skill_id", ydb.PrimitiveType.Utf8),
                ydb.Column(
                    "success_level_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)
                ),
            )
            .with_indexes(
                ydb.TableIndex("success_level_index").with_index_columns(
                    "success_level_id"
                )
            ),
        )

        # subject_presentation
        session.create_table(
            str(path / "subject_presentation"),
            ydb.TableDescription()
            .with_primary_keys("subject_id", "presentation_id")
            .with_columns(
                ydb.Column("subject_id", ydb.PrimitiveType.Utf8),
                ydb.Column("presentation_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # employee
        session.create_table(
            str(path / "employee"),
            ydb.TableDescription()
            .with_primary_keys("employee_id")
            .with_columns(
                ydb.Column("employee_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("first_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("last_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("email", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("gender", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("phone_number", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("avatar_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("tg_user_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("role_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column(
                    "group_ids", ydb.OptionalType(ydb.PrimitiveType.Utf8)
                ),  # Опять дичь какая-то
            )
            .with_indexes(
                ydb.TableIndex("role_index").with_index_columns("role_id"),
            ),
        )

        # parent
        session.create_table(
            str(path / "parent"),
            ydb.TableDescription()
            .with_primary_keys("parent_id")
            .with_columns(
                ydb.Column("parent_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("first_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("last_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column(
                    "email", ydb.OptionalType(ydb.PrimitiveType.Utf8)
                ),  # почему епт фамилия не обязательна, а имейл обязателен?
                ydb.Column("gender", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("phone_number", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column(
                    "freq_notifications", ydb.OptionalType(ydb.PrimitiveType.Uint64)
                ),
                ydb.Column("tg_user_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            )
        )

        # skill_level
        session.create_table(
            str(path / "skill_level"),
            ydb.TableDescription()
            .with_primary_keys("skill_level_id")
            .with_columns(
                ydb.Column("skill_level_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            ),
        )

        # skill
        session.create_table(
            str(path / "skill"),
            ydb.TableDescription()
            .with_primary_keys("skill_id")
            .with_columns(
                ydb.Column("skill_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            ),
        )

        # presentation
        session.create_table(
            str(path / "presentation"),
            ydb.TableDescription()
            .with_primary_keys("presentation_id")
            .with_columns(
                ydb.Column("presentation_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("file_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("photo_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("description", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            ),
        )

        # roles
        session.create_table(
            str(path / "role"),
            ydb.TableDescription()
            .with_primary_keys("role_id")
            .with_columns(
                ydb.Column("role_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            ),
        )

    session_pool.retry_operation_sync(callee)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""create tables script""",
    )
    parser.add_argument(
        "-d", "--database", required=True, help="Name of the database to use"
    )
    parser.add_argument("-e", "--endpoint", required=True, help="Endpoint url to use")
    parser.add_argument("-p", "--path", default="")
    parser.add_argument("-v", "--verbose", default=False, action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logger = logging.getLogger("ydb.pool.Discovery")
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())

    with ydb.Driver(
        endpoint=args.endpoint,
        database=args.database,
        credentials=ydb.credentials_from_env_variables(),
    ) as driver:
        driver.wait(timeout=5, fail_fast=True)
        with ydb.SessionPool(driver) as pool:
            full_path = Path(args.database) / args.path
            create_tables(pool, full_path)
