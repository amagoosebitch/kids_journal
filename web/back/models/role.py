from enum import StrEnum


class Role(StrEnum):
    admin: str = "Администратор"
    teacher: str = "Воспитатель"
    sitter: str = "Нянечка"
