from pydantic import BaseModel


class Object(BaseModel):
    scheme: int


class GetObjectData(Object):
    object_id: int





class FieldScheme(BaseModel):
    id: int
    name: str
    ref: int | None
