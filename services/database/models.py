
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Entity(Base):
    __tablename__ = "entities"

    pk: Mapped[int] = mapped_column(primary_key=True)
    scheme: Mapped[int]
    type_id: Mapped[int]
    name: Mapped[str] = mapped_column(String(32))
    

class Field(Base):
    __tablename__ = "fields"

    pk: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    id: Mapped[int]
