from .connection import Client
from .schemas import EntityScheme, Field, SearchRequest


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
    async def objects(cls, client: Client, entity: EntityScheme):
        json_data = {"scheme": entity.scheme, "method": "attributes", "objectTypeId": entity.item_type}
        response = await client.post("objects/run", json_data)
        return [Field(id=item["id"], name=item["name"]) for item in response.json()]

    def decode(self, obj: dict[int, str], fields: dict) -> dict:
        for attr in obj["attributes"]:
            key = fields.get("attr")
        result: dict[str, str] = {}
        return result


    @classmethod
    def encode(cls):
        pass
