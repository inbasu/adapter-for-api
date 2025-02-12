from abc import ABC, abstractmethod

from services.connections.base import Client
from services.insight_repository.formatters import Formatter

from .schemas import AttrValue, FieldScheme, InsightObject, ObjectAttr


class Unit(ABC):
    _client: Client
    _scheme: int
    _formatter: Formatter

    @abstractmethod
    async def create_object(self, type_id: int, attrs: dict) -> InsightObject | None:
        """ """

    @abstractmethod
    async def get_objects(self, iql: str, page: int, results: int) -> list:
        """ """

    @abstractmethod
    async def update_object(self, type_id: int, object_id: int, attrs: dict) -> InsightObject | None:
        """ """

    @abstractmethod
    async def delete_object(self, object_id: int):
        pass


class InsightMetroUnit(Unit):
    """
    #TODO
    1 - upload_attachment - нет эндпоинта
    2 - get_attachment - нет эндпоинта
    """

    """Object(s) methods"""

    def __init__(self, client: Client, scheme: int, formatter: Formatter) -> None:
        self._client = client
        self._formatter = formatter
        self._scheme = scheme

    async def create_object(self, type_id: int, attrs: dict) -> InsightObject | None:
        json = {"scheme": self._scheme, "objectTypeId": type_id, "attributes": self._form_attributes(attrs)}
        response = await self._client.post("/create/run", data=json)
        return self._formatter.decode_create_object(response.data)

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
            fields = {f["id"]: self._formatter.decode_field(f) for f in response.data.get("objectTypeAttributes", [])}
            entries = response.data.get("objectEntries", [])
            return [self._formatter.decode_get_object(obj, fields) for obj in entries]

    async def update_object(self, type_id: int, object_id: int, attrs: dict) -> InsightObject | None:
        json = {
            "scheme": self._scheme,
            "objectTypeId": type_id,
            "objectId": object_id,
            "attributes": self._form_attributes(attrs),
        }
        response = await self._client.post("/update/run", data=json)
        return self._formatter.decode_update_object(response.data)

    async def delete_object(self, object_id: int):
        pass

    """ Attachment methods """

    async def get_attachment(self):
        raise NotImplementedError()

    async def upload_attachment(self):
        raise NotImplementedError()

    """ Some inclass logic methods """

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
