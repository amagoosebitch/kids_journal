import enum


class EmployeeState(enum.Enum):
    CHOOSE_REPORT_TYPE = 1
    CHOOSE_GROUP = 2
    CHOOSE_CHILD = 3
    WRITE_REPORT = 4
    SEND_PICTURE = 5
    ACCEPT_PRESENTATION = 6


class ParentState(enum.Enum):
    SUBSCRIBE = 10
