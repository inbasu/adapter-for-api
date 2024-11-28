
from .connection import Client
from .schemas import SearchRequest


class Insight:

    @classmethod
    async def read(cls, client: Client, data: SearchRequest) -> list[dict]:
        json_data = {
                "iql": data.iql,
                "scheme": data.scheme,
                "options":{
                    "includeAttributesDeep": 1, # без этого атрибута не отображаются связанные поля
                }
            }
        response = await client.post("iql/run", json_data)
        return response.json().get("objectEntries", [])
    
    def decode(self, obj: dict[int, str], fields: dict) -> dict:
        result: dict[str, str] = {}
        return result


    

