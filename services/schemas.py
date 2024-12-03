from pydantic import BaseModel


class Object(BaseModel):
    scheme: int


class GetObjectData(Object):
    object_id: int

class GetIQLData(Object):
    iql:str 

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

class ObjectResponse(BaseModel):
    id: int
    attrs: list[ObjectAttr]


