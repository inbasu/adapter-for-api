import asyncio
import mimetypes
from typing import Any

from httpx import AsyncClient

from services.connections.connection import Client

from .schemas.insight_schemas import AttrValue, FieldScheme, InsightObject, ObjectAttr


class MetroInsight:
    """Object(s) methods"""

    @classmethod
    async def create_object(cls, client: Client, scheme: int, type_id, attrs: dict) -> InsightObject | None:
        json = {"scheme": scheme, "objectTypeId": type_id, "attributes": cls._form_attributes(attrs)}
        print(json["attributes"])
        response = await client.post("/create/run", data=json)
        print(response.status_code)
        print(response.data)
        if response.status_code == 200:
            try:
                return cls._decode_create_object(response.data)
            except KeyError:
                return None
        return None

    @classmethod
    async def get_objects(
        cls, client: Client, scheme: int, iql: str, page: int = 1, results: int = 500
    ) -> list[InsightObject]:
        json = {
            "scheme": scheme,
            "iql": iql,
            "options": {
                "page": page,
                "resultPerPage": results,
                "includeAttributes": True,
                "includeAttributesDeep": 1,
            },
        }
        response = await client.post("/iql/run", data=json)
        if response.status_code == 200:
            fields = {f["id"]: cls._decode_field(f) for f in response.data.get("objectTypeAttributes", [])}
            entries = response.data.get("objectEntries", [])
            return [cls._decode_get_object(obj, fields) for obj in entries]
        return []

    @classmethod
    async def update_object(
        cls, client: Client, scheme: int, type_id: int, object_id: int, attrs: dict
    ) -> InsightObject | None:
        json = {
            "scheme": scheme,
            "objectTypeId": type_id,
            "objectId": object_id,
            "attributes": cls._form_attributes(attrs),
        }
        response = await client.post("/update/run", data=json)
        if response.status_code == 200:
            return cls._decode_update_object(response.data)
        return None

    @classmethod
    def _decode_field(cls, field: dict) -> FieldScheme:
        return FieldScheme(id=field["id"], name=field["name"], ref=field.get("referenceObjectTypeId", None))

    @classmethod
    def _form_attributes(cls, attrs: dict) -> list[dict]:
        return [
            {
                "objectTypeAttributeId": id,
                "objectAttributeValues": [
                    [{"value": value} for value in values] if isinstance(values, list) else {"value": values}
                ],
            }
            for id, values in attrs.items()
        ]

    @classmethod
    def _decode_create_object(cls, raw_object: dict) -> InsightObject:
        return InsightObject(id=raw_object["id"], label=raw_object["label"], attrs=[])

    @classmethod
    def _decode_get_object(cls, raw_object: dict, fields: dict[int, FieldScheme]) -> InsightObject:
        obj = InsightObject(id=raw_object["id"], label=raw_object["label"], attrs=[])
        for attr in raw_object["attributes"]:
            object_attr = ObjectAttr(
                id=attr["objectTypeAttributeId"],
                name=fields[attr["objectTypeAttributeId"]].name,
                ref=fields[attr["objectTypeAttributeId"]].ref,
                values=[],
            )
            for val in attr["objectAttributeValues"]:
                object_attr.values.append(
                    AttrValue(id=val["referencedObject"]["id"] if object_attr.ref else None, label=val["displayValue"])
                )
            obj.attrs.append(object_attr)
        return obj

    @classmethod
    def _decode_update_object(cls, raw_object: dict) -> InsightObject:
        obj = InsightObject(id=raw_object["id"], label=raw_object["label"], attrs=[])
        for attr in raw_object["attributes"]:
            object_attr = ObjectAttr(
                id=attr["objectTypeAttributeId"],
                name=attr["objectTypeAttribute"]["name"],
                ref=attr.get("referenceObjectTypeId", None),
                values=[],
            )
            for val in attr["objectAttributeValues"]:
                object_attr.values.append(
                    AttrValue(id=val["referencedObject"]["id"] if object_attr.ref else None, label=val["displayValue"])
                )
            obj.attrs.append(object_attr)
        return obj
