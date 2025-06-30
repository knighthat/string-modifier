from enum import Enum


class FileType(Enum):
    STRINGS = 0
    PLURALS = 1

class Actions(Enum): 
    ADD = 0
    REMOVE = 1
    MODIFY = 2