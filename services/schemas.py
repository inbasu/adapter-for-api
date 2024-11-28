from pydantic import BaseModel


class SearchRequest(BaseModel):
    scheme: int 
    item_type: int | str
    iql: str

class EntityScheme(BaseModel):
    scheme: int
    item_type: int
    name: str


class Field(BaseModel):
    name: str
    id: int

class Entity(BaseModel):
    scheme: int
    type_id: int
    name: str
