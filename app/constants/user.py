import enum

class RoleEnum(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"