from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.properties import ForeignKey


class Base(DeclarativeBase):
    pass

class InsightEntity(Base):
    __tablename__ = "entities"
    
    pk: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    schema: Mapped[int]
    type_id: Mapped[int]

class InsightField(Base):
    __tablename__ = "fields"

    pk: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    id: Mapped[int]
    # Many to Many or foreng key?
    rel_to: Mapped[Optional[int]] = mapped_column(ForeignKey("entities.pk"))



