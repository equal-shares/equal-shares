from enum import Enum


class Gender(Enum):
    """
    >>> Gender.MALE.value
    1
    >>> Gender.FEMALE.value
    2
    >>> Gender.MALE.name
    'MALE'
    >>> Gender.FEMALE.name
    'FEMALE'
    """

    MALE = 1
    FEMALE = 2
