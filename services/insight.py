
from .connection import Client
from .schemas import SearchRequest


class Insight:

    @classmethod
    async def read(cls, client: Client, data: SearchRequest) -> list[dict]:
        return [{}]
    
    def decode(self, obj: dict[int, str], fields: dict) -> dict:
        return {fields[key]: value for key,value in obj.items()}
