from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import Integer


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = str(cls.__name__)
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_') + 's'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

