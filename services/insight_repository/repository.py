from services.connections.base import Client

from .schemas import AttrValue, FieldScheme, InsightObject, ObjectAttr


class MetroRepository:
    """Object(s) methods"""

    def __init__(self, client: Client, scheme: int) -> None:
        self._client = client
        self._scheme = scheme

    async def create_object(self, type_id, attrs: dict) -> InsightObject | None:
        json = {"scheme": self._scheme, "objectTypeId": type_id, "attributes": self._form_attributes(attrs)}
        response = await self._client.post("/create/run", data=json)
        if response.status_code == 200:
            try:
                return self._decode_create_object(response.data)
            except KeyError:
                return None
        return None

    async def get_objects(self, iql: str, page: int = 1, results: int = 500) -> list[InsightObject]:
        json = {
            "scheme": self._scheme,
            "iql": iql,
            "options": {
                "page": page,
                "resultPerPage": results,
                "includeAttributes": True,
                "includeAttributesDeep": 1,
            },
        }
        response = await self._client.post("/iql/run", data=json)
        if response.status_code == 200:
            fields = {f["id"]: self._decode_field(f) for f in response.data.get("objectTypeAttributes", [])}
            entries = response.data.get("objectEntries", [])
            return [self._decode_get_object(obj, fields) for obj in entries]
        return []

    async def update_object(self, type_id: int, object_id: int, attrs: dict) -> InsightObject | None:
        json = {
            "scheme": self._scheme,
            "objectTypeId": type_id,
            "objectId": object_id,
            "attributes": self._form_attributes(attrs),
        }
        response = await self._client.post("/update/run", data=json)
        if response.status_code == 200:
            return self._decode_update_object(response.data)
        return None

    def _decode_field(self, field: dict) -> FieldScheme:
        return FieldScheme(id=field["id"], name=field["name"], ref=field.get("referenceObjectTypeId", None))

    def _form_attributes(self, attrs: dict) -> list[dict]:
        return [
            {
                "objectTypeAttributeId": id,
                "objectAttributeValues": [
                    [{"value": value} for value in values] if isinstance(values, list) else {"value": values}
                ],
            }
            for id, values in attrs.items()
        ]

    def _decode_create_object(self, raw_object: dict) -> InsightObject:
        return InsightObject(id=raw_object["id"], label=raw_object["label"], attrs=[])

    def _decode_get_object(self, raw_object: dict, fields: dict[int, FieldScheme]) -> InsightObject:
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

    def _decode_update_object(self, raw_object: dict) -> InsightObject:
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
