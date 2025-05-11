import re
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import Integer, func

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        class_name = cls.__name__.replace("Model", "")

        # Разбиваем по заглавным буквам (CamelCase -> snake_case)
        name_snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()

        if name_snake_case.endswith("y"):
            return name_snake_case[:-1] + "ies"

        return name_snake_case + "s"