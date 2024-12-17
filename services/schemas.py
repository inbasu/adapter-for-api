from typing import Any

from pydantic import BaseModel


class Object(BaseModel):
    scheme: int


class GetObjectData(Object):
    object_id: int

class GetIQLData(Object):
    iql:str 

class GetJoinedData(GetIQLData):
    joined_iql: str
    on: str
    

class FieldScheme(BaseModel):
    id: int
    name: str
    ref: int | None


class UpdateObjectData(GetObjectData):
    object_type_id: int
    attrs: dict[int, list[Any]]





# Схемы для формирвания объекта
class AttrValue(BaseModel):
    id: int | None
    label: str

class ObjectAttr(BaseModel):
    id: int
    name: str
    values: list[AttrValue] 
    ref: int | None

class ObjectResponse(BaseModel):
    id: int
    label: str
    attrs: list[ObjectAttr]
    joined: list["ObjectResponse"] = []
    

    def get_field_values(self, field_name: str) -> list[AttrValue]:
        for attr in self.attrs:
            if attr.name == field_name:
                return attr.values
        return []
