
import asyncio
import mimetypes
from typing import Any

from requests_toolbelt.multipart.encoder import MultipartEncoder

from .connections.insight_api_connection import InsightAPIClient
from .connections.mars_connection import MarsClient, Responce
from .schemas.insight_schemas import (AttrValue, FieldScheme, GetIQLData,
                                      GetJoinedData, GetObjectData,
                                      InsightObject, ObjectAttr,
                                      UpdateObjectData)


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
    async def get_object(cls, client: MarsClient, data: GetObjectData) -> InsightObject | None:
        # перенести fields внутрь локиги класса
        json =  cls.form_json(scheme=data.scheme, iql=f"objectId = {data.object_id}", page=1, result_per_page=1)
        result = await client.post('/ru-insight/iql/run',data=json)
        if raw_data := result.json():
            fields = {f["id"]: cls.decode_field(f) for f in raw_data.get("objectTypeAttributes", [])}
            return cls.decode(raw_data.get("objectEntries")[0], fields)
        return None
    
    @classmethod
    async def get_objects(cls, client: MarsClient, data: GetIQLData) -> list[InsightObject]:
        json = cls.form_json(scheme=data.scheme, iql=data.iql, result_per_page=100, page=1)
        result = await client.post("/ru-insight/iql/run", data=json)
        return cls.decode_objects(result)

    @classmethod
    async def get_joined(cls, client: MarsClient, data: GetJoinedData) -> list[InsightObject]:
        main_json = cls.form_json(scheme=data.scheme, iql=data.iql, result_per_page=100, page=1)
        joined_json = cls.form_json(scheme=data.scheme, iql=f'{data.joined_iql} AND object HAVING outboundReferences({data.iql})', result_per_page=100, page=1)
        main, join = await asyncio.gather(
                client.post('/ru-insight/iql/run', data=main_json),
                client.post('/ru-insight/iql/run', data=joined_json),
                )
        result: list[InsightObject] = cls.decode_objects(main)

        if to_join := cls.decode_objects(join):
            for obj in result:
                for rel in to_join:
                    if obj.id in [r.id for r in rel.get_field_values(data.on)]:
                        obj.joined.append(rel)
        return result


    @classmethod
    async def update_object(cls, client: MarsClient, data: UpdateObjectData) -> InsightObject | None:
        json = {"scheme": data.scheme, "objectTypeId": data.object_type_id, "objectId": data.object_id, 
                "attributes": [{"objectTypeAttributeId": id, 
                                "objectAttributeValues": [{"value": value} for value in values]}
                               for id, values in data.attrs.items()]}
        result = await client.post('/ru-insight/update/run', data=json)
        if raw_data := result.json():
            return cls.decode_upd_or_cr(raw_data)
        return None

        


    @classmethod
    async def create_object(cls, client: MarsClient, data: UpdateObjectData) -> InsightObject | None:
        json = {"scheme": data.scheme, "objectTypeId": data.object_type_id,
                "attributes": [{"objectTypeAttributeId": id, 
                                "objectAttributeValues": [{"value": value for value in values}]}
                               for id, values in data.attrs.items()]}
        result = await client.post('/ru-insight/create/run', data=json)
        if raw_data := result.json():
            return cls.decode_upd_or_cr(raw_data)
        return None



    @classmethod
    async def add_attachment(cls, client: InsightAPIClient, data, file, name, mimetype):
        mimetypes.init()
        json = MultipartEncoder({'encodedComment': '', "file": (name, file, mimetype)})
        result = await client.post('', data=data, content_type=json.content_type)
        return result
    
    @classmethod
    async def download_attachment(cls, client: InsightAPIClient, url: str):
        pass



    @classmethod
    async def get_object_fields(cls, client: MarsClient, data: GetObjectData) -> list[FieldScheme]:
        json = {"scheme": data.scheme, "method": "attributes", "objectTypeId": data.object_id}
        result = await client.post("/ru-insight/objects/run", data=json)
        return [cls.decode_field(field) for field in result.json()]


    @classmethod
    def decode_objects(cls, data: Responce) -> list[InsightObject]:
        if raw_data := data.json():
            fields = {f["id"]: cls.decode_field(f) for f in raw_data.get("objectTypeAttributes", [])}
            return [cls.decode(obj, fields) for obj in raw_data.get("objectEntries", [])]
        return []

    @classmethod
    def decode_field(cls, field: dict) -> FieldScheme:
        return FieldScheme(id=field["id"], name=field["name"], ref=field.get("referenceObjectTypeId", None))
    


    @classmethod
    def decode(cls, raw_object: dict, fields: dict[int, FieldScheme]) -> InsightObject:
        obj = InsightObject(id=raw_object["id"], label=raw_object["label"], attrs=[])
        for attr in raw_object["attributes"]:
            object_attr = ObjectAttr(id=attr["objectTypeAttributeId"], 
                                     name=fields[attr["objectTypeAttributeId"]].name,
                                     ref=fields[attr["objectTypeAttributeId"]].ref, values=[])      
            for val in attr["objectAttributeValues"]:
                object_attr.values.append(AttrValue(id=val["referencedObject"]['id'] if object_attr.ref else None,
                                                    label=val["displayValue"]))
            obj.attrs.append(object_attr)
        return obj

            
    @classmethod
    def decode_upd_or_cr(cls, raw_object: dict) -> InsightObject:
        obj = InsightObject(id=raw_object["id"], label=raw_object['label'], attrs=[])
        for attr in raw_object["attributes"]:
            object_attr = ObjectAttr(id=attr["objectTypeAttributeId"],
                                     name=attr["objectTypeAttribute"]['name'],
                                     ref=attr.get("referenceObjectTypeId", None), values=[]
                                     )
            for val in attr["objectAttributeValues"]:
                object_attr.values.append(AttrValue(id=val["referencedObject"]['id'] if object_attr.ref else None,
                                                    label=val["displayValue"]))
            obj.attrs.append(object_attr)
        return obj
