from typing import Any

from .connection import Client
from .schemas import GetObjectData


class Insight:
    
    @classmethod
    def form_json(cls, scheme: int, iql: str,result_per_page:int ,page: int, deep: int=1) -> dict[str, Any]:
        return {
                "scheme": scheme,
                "iql": iql,
                "options": {
                    "page": page,
                    "resultPerPage": result_per_page,
                    "includeAtributes": True,
                    "includeAtributesDeep": deep,
                    },
                }



    @classmethod
    async def get_object(cls, client: Client, data: GetObjectData) -> dict:
        json =  cls.form_json(scheme=data.scheme, iql=f"objectId = {data.object_id}", page=1, result_per_page=1)
        result = await client.post('iql/run',data=json)
        raw_object = result.json()
        return raw_object
