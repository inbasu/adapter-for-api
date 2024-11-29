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
        return raw_object.get("objectEntries", [{}])[0]


#     @classmethod
#     async def get_objects(cls, client: Client, data: GetManyObjectsData) -> list[dict]:
#         json = cls.form_json()
#         result = await client.post("iql/run", data=json)




    @classmethod
    def decode(cls, raw_object: dict, fields: dict) -> dict[str, dict]:
        # Переделать на инпейс

        result: dict[str, dict] = {}
        


        for attr in raw_object["attributes"]:
            key: str = fields.get(attr["objectAtributeId"])
            value: dict[str, Any] = {"value": [], "rederence": None}
            for a in attr["objectAtributeValues"]:
                if a["referencedType"]:
                    value["reference"] = 1 
                    value["value"].append({"label": a["displayValue"], "id": 123321})
                else:
                    pass
            result[key] = value
        return result

        
    

a = {
"id": 12332,
"attrs":[{
    "name": 'some name',        
    "id": 3123123,
    "value": [{"label":"some", "id": 123123}],
    "reference": 321321,
    }]
}
print(a)
