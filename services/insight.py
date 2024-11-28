
import json

from .connection import Client
from .schemas import SearchRequest


class Insight:

    @classmethod
    async def read(cls, client: Client, data: SearchRequest) -> list[dict]:
        insight_response = await client.post("iql/run", data.model_dump())
        if result := insight_response.json().get("result", ""):
            return json.loads(result).get("objectEntries", [])
        return []
    
    def decode(self, obj: dict[int, str], fields: dict) -> dict:
        return {fields[key]: value for key,value in obj.items()}
