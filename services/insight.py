from typing import Any

from .connection import Client
from .schemas import (AttrValue, FieldScheme, GetObjectData, ObjectAttr,
                      ObjectResponse)


class Insight:    
    @classmethod
    def form_json(cls, scheme: int, iql: str,result_per_page:int ,page: int, deep: int=1) -> dict[str, Any]:
        return {
                "scheme": scheme,
                "iql": iql,
                "options": {
                    "page": page,
                    "resultPerPage": result_per_page,
                    "includeAttributes": True,
                    "includeAttributesDeep": deep,
                    },
                }



    @classmethod
    async def get_object(cls, client: Client, data: GetObjectData) -> ObjectResponse | None:
        json =  cls.form_json(scheme=data.scheme, iql=f"objectId = {data.object_id}", page=1, result_per_page=1)
        result = await client.post('iql/run',data=json)
        raw_object = result.json()
        return cls.decode(raw_object["objectEntries"][0]) if raw_object.get("objectEntries", None) else None


    @classmethod
    async def get_object_fields(cls, client: Client, data: GetObjectData):
        json = {"scheme": data.scheme, "method": "attributes", "objectTypeId": data.object_id}
        result = await client.post("objects/run", data=json)
        return [cls.decode_field(field) for field in result.json()]




    @classmethod
    def decode(cls, raw_object: dict) -> ObjectResponse:
        obj = ObjectResponse(id=raw_object["id"], attrs=[])
        # Переделать на инпейс
        for attr in raw_object["attributes"]:
            value = ObjectAttr(id=attr["objectTypeAttributeId"], name="", ref=None, values=[])      
            for a in attr["objectAttributeValues"]:
                if a["referencedType"]:
                    value.ref = a["referencedObject"]["objectType"]["id"]
                    value.values.append(AttrValue(id=a["referencedObject"]['id'], label=a["displayValue"]))
                else:
                    value.values.append(AttrValue(id=None, label=a["displayValue"]))
            obj.attrs.append(value)
        return obj


    @classmethod
    def decode_field(cls, field: dict) -> FieldScheme:
        return FieldScheme(id=field["id"], name=field["name"], ref=field.get("referenceObjectTypeId", None))
    


