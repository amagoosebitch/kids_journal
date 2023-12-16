import argparse
import logging
from pathlib import Path
from typing import Any

import ydb


def create_tables(session_pool: Any, path: Path):
    def callee(session: Any):
        # organization
        session.create_table(
            path / "organization",
            ydb.TableDescription()
            .with_primary_keys("organization_id")
            .with_columns(
                ydb.Column("organization_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.PrimitiveType.Utf8),
                ydb.Column("description", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("photo_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("start_education_time", ydb.PrimitiveType.Datetime),
                ydb.Column("end_education_time", ydb.PrimitiveType.Datetime),
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
            path / "group",
            ydb.TableDescription()
            .with_primary_keys("group_id")
            .with_columns(
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("organization_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.PrimitiveType.Utf8),
                ydb.Column("age_range", ydb.PrimitiveType.Uint64),
            )
            .with_indexes(
                ydb.TableIndex("organization_index").with_index_columns(
                    "organization_id"
                )
            ),
        )

        # group_teacher
        session.create_table(
            path / "group_teacher",
            ydb.TableDescription()
            .with_primary_keys("group_id", "teacher_id")  # точно оба форяки ?
            .with_columns(
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("teacher_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # group_child
        session.create_table(
            path / "group_child",
            ydb.TableDescription()
            .with_primary_keys("group_id", "child_id")  # точно оба форяки ?
            .with_columns(
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("child_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # group_subject
        session.create_table(
            path / "group_subject",
            ydb.TableDescription()
            .with_primary_keys("group_id", "subject_id")  # точно оба форяки ?
            .with_columns(
                ydb.Column("group_id", ydb.PrimitiveType.Utf8),
                ydb.Column("subject_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # child
        session.create_table(
            path / "child",
            ydb.TableDescription()
            .with_primary_keys("child_id")
            .with_columns(
                ydb.Column("child_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.PrimitiveType.Utf8),
                ydb.Column("first_name", ydb.PrimitiveType.Utf8),
                ydb.Column("last_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("birth_date", ydb.OptionalType(ydb.PrimitiveType.Date)),
                ydb.Column(
                    "start_education_date", ydb.OptionalType(ydb.PrimitiveType.Date)
                ),
                ydb.Column(
                    "start_education_time",
                    ydb.OptionalType(ydb.PrimitiveType.Timestamp),
                ),
                ydb.Column(
                    "end_education_time", ydb.OptionalType(ydb.PrimitiveType.Timestamp)
                ),
                ydb.Column("gender", ydb.OptionalType(ydb.PrimitiveType.Uint8)),
                ydb.Column("parent_1", ydb.OptionalType(ydb.PrimitiveType.Uint8)),
                ydb.Column("parent_2", ydb.OptionalType(ydb.PrimitiveType.Uint8)),
            ),
        )

        # subject
        session.create_table(
            path / "subject",
            ydb.TableDescription()
            .with_primary_keys("subject_id")
            .with_columns(
                ydb.Column("subject_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.PrimitiveType.Utf8),
                ydb.Column("description", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("age_range", ydb.PrimitiveType.Uint64),
            ),
        )

        # child_skills
        session.create_table(
            path / "child_skills",
            ydb.TableDescription()
            .with_primary_keys("child_id", "skill_id")
            .with_columns(
                ydb.Column("child_id", ydb.PrimitiveType.Utf8),
                ydb.Column("skill_id", ydb.PrimitiveType.Utf8),
                ydb.Column("success_level_id", ydb.PrimitiveType.Utf8),
            )
            .with_indexes(
                ydb.TableIndex("success_level_index").with_index_columns(
                    "success_level_id"
                )
            ),
        )

        # subject_presentation
        session.create_table(
            path / "subject_presentation",
            ydb.TableDescription()
            .with_primary_keys("subject_id", "presentation_id")
            .with_columns(
                ydb.Column("subject_id", ydb.PrimitiveType.Utf8),
                ydb.Column("presentation_id", ydb.PrimitiveType.Utf8),
            ),
        )

        # employee
        session.create_table(
            path / "employee",
            ydb.TableDescription()
            .with_primary_keys("employee_id")
            .with_columns(
                ydb.Column("employee_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.PrimitiveType.Utf8),
                ydb.Column("first_name", ydb.PrimitiveType.Utf8),
                ydb.Column("last_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("email", ydb.PrimitiveType.Utf8),
                ydb.Column("gender", ydb.OptionalType(ydb.PrimitiveType.Uint8)),
                ydb.Column("phone_number", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("avatar_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("tg_user_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("role_id", ydb.PrimitiveType.Utf8),
            )
            .with_indexes(
                ydb.TableIndex("tg_user_index").with_index_columns("tg_user_id"),
                ydb.TableIndex("role_index").with_index_columns("role_id"),
            ),
        )

        # parent
        session.create_table(
            path / "parent",
            ydb.TableDescription()
            .with_primary_keys("parent_id")
            .with_columns(
                ydb.Column("parent_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.PrimitiveType.Utf8),
                ydb.Column("first_name", ydb.PrimitiveType.Utf8),
                ydb.Column("last_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column(
                    "email", ydb.PrimitiveType.Utf8
                ),  # почему епт фамилия не обязательна, а имейл обязателен?
                ydb.Column("gender", ydb.PrimitiveType.Uint8),
                ydb.Column("phone_number", ydb.PrimitiveType.Utf8),
                ydb.Column(
                    "freq_notifications", ydb.OptionalType(ydb.PrimitiveType.Uint64)
                ),
                ydb.Column("tg_user_id", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            )
            .with_indexes(
                ydb.TableIndex("tg_user_index").with_index_columns("tg_user_id"),
            ),
        )

        # skill_level
        session.create_table(
            path / "skill_level",
            ydb.TableDescription()
            .with_primary_keys("skill_level_id")
            .with_columns(
                ydb.Column("skill_level_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.PrimitiveType.Utf8),
            ),
        )

        # skill
        session.create_table(
            path / "skill",
            ydb.TableDescription()
            .with_primary_keys("skill_id")
            .with_columns(
                ydb.Column("skill_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.PrimitiveType.Utf8),
            ),
        )

        # presentation
        session.create_table(
            path / "presentation",
            ydb.TableDescription()
            .with_primary_keys("presentation_id")
            .with_columns(
                ydb.Column("presentation_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.PrimitiveType.Utf8),
                ydb.Column("file_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("photo_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("description", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
            ),
        )

        # roles
        session.create_table(
            path / "role",
            ydb.TableDescription()
            .with_primary_keys("role_id")
            .with_columns(
                ydb.Column("role_id", ydb.PrimitiveType.Utf8),
                ydb.Column("name", ydb.PrimitiveType.Utf8),
            ),
        )

        # tg_user???
        session.create_table(
            path / "tg_user",
            ydb.TableDescription()
            .with_primary_keys("tg_user_id")
            .with_columns(
                ydb.Column("tg_user_id", ydb.PrimitiveType.Utf8),
                ydb.Column("first_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("last_name", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("username", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
                ydb.Column("photo_url", ydb.OptionalType(ydb.PrimitiveType.Utf8)),
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
