
from .connection import Client
from .schemas import Field, SearchRequest


class Insight:

    @classmethod
    async def read(cls, client: Client, data: SearchRequest) -> list[dict]:
        json_data = {
                "iql": data.iql,
                "scheme": data.scheme,
                "options":{
                    "includeAttributes": True,
                    "includeAttributesDeep": 1, # без этого атрибута не отображаются связанные поля
                }
            }
        response = await client.post("iql/run", json_data)
        return response.json().get("objectEntries", [])
    
    


    @classmethod
    async def objects(cls, client: Client):
        json_data = {"scheme": 10, "method": "attributes", "objectTypeId": 155}
        response = await client.post("objects/run", json_data)
        return [Field(id=item["id"], name=item["name"]) for item in response.json()]





    def decode(self, obj: dict[int, str], fields: dict) -> dict:

        result: dict[str, str] = {}
        return result


    

