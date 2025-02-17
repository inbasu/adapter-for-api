from typing import Any

from pydantic import BaseModel


class FieldScheme(BaseModel):
    id: int
    name: str
    ref: int | None


# Схемы для формирвания объекта
class AttrValue(BaseModel):
    id: int | None
    label: str


class ObjectAttr(BaseModel):
    id: int
    name: str
    values: list[AttrValue]
    ref: int | None


class InsightObject(BaseModel):
    id: int
    label: str
    attrs: list[ObjectAttr]
    joined: list["InsightObject"] = []

    def get_field_values(self, field_name: str) -> list[AttrValue]:
        for attr in self.attrs:
            if attr.name == field_name:
                return attr.values
        return []

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id
