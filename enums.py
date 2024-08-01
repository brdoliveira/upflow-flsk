from enum import Enum

class PermissionLevel(Enum):
    ADMIN = 1
    EDITOR = 2
    VIEWER = 3
    GUEST = 4