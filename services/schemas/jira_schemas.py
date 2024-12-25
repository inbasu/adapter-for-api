from typing import Any

from pydantic import BaseModel


class AddAttachment(BaseModel):
    project: str
    issue: str
    name: str
    source: str

class Field(BaseModel):
    name: str
    value: Any

