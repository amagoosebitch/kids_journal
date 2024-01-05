import enum


class ReportTypeCallback(enum.StrEnum):
    SINGLE_CHILD = "Отчёт по ребенку"
    COMMON = "Общий отчёт"
    OBSERVATION = "Наблюдение"
