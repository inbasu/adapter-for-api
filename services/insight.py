from typing import Any

from .connection import Client
from .schemas import (AttrValue, FieldScheme, GetIQLData, GetObjectData,
                      ObjectAttr, ObjectResponse)


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
        # перенести fields внутрь локиги класса
        json =  cls.form_json(scheme=data.scheme, iql=f"objectId = {data.object_id}", page=1, result_per_page=1)
        result = await client.post('iql/run',data=json)
        if raw_data := result.json():
            fields = {f["id"]: cls.decode_field(f) for f in raw_data.get("objectTypeAttributes")}
            return cls.decode(raw_data.get("objectEntries")[0], fields)
        return None
    
    @classmethod
    async def get_objects(cls, client: Client, data: GetIQLData) -> list[ObjectResponse]:
        json = cls.form_json(scheme=data.scheme, iql=data.iql, result_per_page=100, page=1)
        result = await client.post("iql/run", data=json)
        if raw_data := result.json():
            fields = {f["id"]: cls.decode_field(f) for f in raw_data.get("objectTypeAttributes")}
            return [cls.decode(obj, fields) for obj in raw_data.get("objectEntries")]
        return []

    @classmethod
    async def get_object_fields(cls, client: Client, data: GetObjectData) -> list[FieldScheme]:
        json = {"scheme": data.scheme, "method": "attributes", "objectTypeId": data.object_id}
        result = await client.post("objects/run", data=json)
        return [cls.decode_field(field) for field in result.json()]



    @classmethod
    def decode_field(cls, field: dict) -> FieldScheme:
        return FieldScheme(id=field["id"], name=field["name"], ref=field.get("referenceObjectTypeId", None))
    


    @classmethod
    def decode(cls, raw_object: dict, fields: dict[int, FieldScheme]) -> ObjectResponse:
        obj = ObjectResponse(id=raw_object["id"], attrs=[])
        for attr in raw_object["attributes"]:
            object_attr = ObjectAttr(id=attr["objectTypeAttributeId"], 
                                     name=fields[attr["objectTypeAttributeId"]].name, 
                                     ref=fields[attr["objectTypeAttributeId"]].ref, values=[])      
            for val in attr["objectAttributeValues"]:
                object_attr.values.append(AttrValue(id=val["referencedObject"]['id'] if object_attr.ref else None, 
                                                    label=val["displayValue"]))
            obj.attrs.append(object_attr)
        return obj

            

