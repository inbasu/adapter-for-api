from pydantic import BaseModel


class SearchRequest(BaseModel):
    scheme: int 
    item_type: int | str
    iql: str
