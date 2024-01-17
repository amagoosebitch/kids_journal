import enum


class AgeRanges(enum.StrEnum):
    ZERO_THREE = "0-3"
    TWO_SIX = "3-6"
    SIX_PLUS = "6-9"


class Gender(enum.StrEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
