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

        # organizations_users
        session.create_table(
            str(path / "organizations_users"),
            ydb.TableDescription()
            .with_primary_keys("organization_id", "user_id")
            .with_columns(
                ydb.Column("organization_id", ydb.PrimitiveType.Utf8),
                ydb.Column("user_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # organizations_admins
        session.create_table(
            str(path / "organizations_admins"),
            ydb.TableDescription()
            .with_primary_keys("organization_id", "user_id")
            .with_columns(
                ydb.Column("organization_id", ydb.PrimitiveType.Utf8),
                ydb.Column("user_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # group
        session.create_table(
            str(path / "group"),
            ydb.TableDescription()
            .with_primary_key("group_id")
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
            .with_primary_keys("group_id", "teacher_id")
            .with_columns(
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("teacher_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # group_child
        session.create_table(
            str(path / "group_child"),
            ydb.TableDescription()
            .with_primary_keys("group_id", "child_id")
            .with_columns(
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("child_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # group_subject
        session.create_table(
            str(path / "group_subject"),
            ydb.TableDescription()
            .with_primary_keys("group_id", "subject_id")
            .with_columns(
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("subject_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # child
        session.create_table(
            str(path / "child"),
            ydb.TableDescription()
            .with_primary_key("child_id")
            .with_columns(
                ydb.Column("child_id", ydb.PrimitiveType.Utf8),
                ydb.Column("first_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("middle_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("last_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("birth_date", ydb.OptionalType(ydb.PrimitiveType.Date)),
                ydb.Column(
                    "start_education_date", ydb.OptionalType(ydb.PrimitiveType.Date)
                ),
                ydb.Column(
                    "end_education_date", ydb.OptionalType(ydb.PrimitiveType.Date)
                ),
                ydb.Column("gender", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("avatar_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            ),
        )

        # child_parent
        session.create_table(
            str(path / "child_parent"),
            ydb.TableDescription()
            .with_primary_keys("child_id", "parent_id")
            .with_columns(
                ydb.Column("child_id", ydb.PrimitiveType.Utf8),
                ydb.Column("parent_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # child_schedule
        session.create_table(
            str(path / "child_schedule"),
            ydb.TableDescription()
            .with_primary_keys("child_id", "schedule_id")
            .with_columns(
                ydb.Column("child_id", ydb.PrimitiveType.Utf8),
                ydb.Column("schedule_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # schedule
        session.create_table(
            str(path / "schedule"),
            ydb.TableDescription()
            .with_primary_key("schedule_id")
            .with_columns(
                ydb.Column("schedule_id", ydb.PrimitiveType.Utf8),
                ydb.Column(
                    "start_lesson", ydb.OptionalType(ydb.PrimitiveType.Datetime)
                ),
                ydb.Column("end_lesson", ydb.OptionalType(ydb.PrimitiveType.Datetime)),
                ydb.Column("presentation_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("canceled", ydb.OptionalType(ydb.PrimitiveType.Bool)),
            ),
        )

        # group_schedule
        session.create_table(
            str(path / "group_schedule"),
            ydb.TableDescription()
            .with_primary_keys("group_id", "schedule_id")
            .with_columns(
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("schedule_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # note
        session.create_table(
            str(path / "note"),
            ydb.TableDescription()
            .with_primary_key("note_id")
            .with_columns(
                ydb.Column("note_id", ydb.PrimitiveType.Utf8),
                ydb.Column("presentation_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("child_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("user_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("text", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            ),
        )

        # subject
        session.create_table(
            str(path / "subject"),
            ydb.TableDescription()
            .with_primary_key("subject_id")
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
            .with_primary_keys("child_id", "presentation_id")
            .with_columns(
                ydb.Column("child_id", ydb.PrimitiveType.Utf8),
                ydb.Column("presentation_id", ydb.PrimitiveType.Utf8),
                ydb.Column("skill_level_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            )
            .with_indexes(
                ydb.TableIndex("skill_level_index").with_index_columns("skill_level_id")
            ),
        )

        # user
        session.create_table(
            str(path / "user"),
            ydb.TableDescription()
            .with_primary_key("user_id")
            .with_columns(
                ydb.Column("user_id", ydb.PrimitiveType.Utf8),
                ydb.Column("first_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("middle_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("last_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("email", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("gender", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("phone_number", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("avatar_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("tg_user_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            )
            .with_index(
                ydb.TableIndex("user_index_by_tg_user_id").with_index_columns(
                    "tg_user_id"
                )
            )
            .with_index(
                ydb.TableIndex("user_index_by_phone_number").with_index_columns(
                    "phone_number"
                )
            ),
        )

        # skill_level
        session.create_table(
            str(path / "skill_level"),
            ydb.TableDescription()
            .with_primary_key("skill_level_id")
            .with_columns(
                ydb.Column("skill_level_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("description", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            ),
        )

        # presentation
        session.create_table(
            str(path / "presentation"),
            ydb.TableDescription()
            .with_primary_key("presentation_id")
            .with_columns(
                ydb.Column("presentation_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("file_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("photo_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("description", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("subject_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            ),
        )

        # user_role
        session.create_table(
            str(path / "user_role"),
            ydb.TableDescription()
            .with_primary_keys("user_id", "role")
            .with_columns(
                ydb.Column("user_id", ydb.PrimitiveType.Utf8),
                ydb.Column("role", ydb.PrimitiveType.Utf8),
            ),
        )

        # tg_user
        session.create_table(
            str(path / "tg_user"),
            ydb.TableDescription()
            .with_primary_keys("tg_user_id", "username")
            .with_columns(
                ydb.Column("tg_user_id", ydb.PrimitiveType.Utf8),
                ydb.Column("username", ydb.PrimitiveType.Utf8),
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
