from enum import Enum


class Priority(float, Enum):
    HIG = 0.4
    MID = 0.7
    LOW = 1
