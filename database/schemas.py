from pydantic import BaseModel


class Field(BaseModel):
    name: str
    id: int
