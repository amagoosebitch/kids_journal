import enum


class AgeRanges(enum.StrEnum):
    ZERO_TWO = "0-2"
    TWO_FOUR = "2-4"
    FOUR_SIX = "4-6"


class Gender(enum.StrEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
