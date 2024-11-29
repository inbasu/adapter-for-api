from pydantic import BaseModel


class GetObjectData(BaseModel):
    scheme: int
    object_id: int
