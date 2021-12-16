from enum import Enum


class MARKER(Enum):
    UPDATES = 1
    MESSAGE = 2

    def __str__(self):
        return super.__str__(self).replace("<MARKER.", "").split(":")[0]
