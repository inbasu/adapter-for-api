from abc import ABC, abstractmethod
from typing import Any, Callable

from services.insight_repository.schemas import AttrValue, FieldScheme, InsightObject, ObjectAttr


class Formatter(ABC):
    """ """

    @classmethod
    @abstractmethod
    def decode_create_object(cls, object: dict):
        """ """

    @classmethod
    @abstractmethod
    def decode_get_object(cls, object: dict, fields: dict[int, FieldScheme]):
        """ """

    @classmethod
    @abstractmethod
    def decode_update_object(cls, object: dict):
        """ """

    @classmethod
    def decode_field(cls, field: dict) -> FieldScheme:
        return FieldScheme(id=field["id"], name=field["name"], ref=field.get("referenceObjectTypeId", None))

    @staticmethod
    def key_error_possible(decode: Callable):
        def wrapper(*args, **kwargs):
            try:
                return decode(*args, **kwargs)
            except KeyError:
                return None

        return wrapper


class DefaultAssetToolFormatter(Formatter):
    @classmethod
    @Formatter.key_error_possible
    def decode_create_object(cls, object: dict):
        try:
            return InsightObject(id=object["id"], label=object["label"], attrs=[])
        except KeyError:
            return None

    @classmethod
    @Formatter.key_error_possible
    def decode_get_object(cls, object: dict, fields: dict[int, FieldScheme]):
        return InsightObject(
            id=object["id"],
            label=object["label"],
            attrs=[
                ObjectAttr(
                    id=attr["objectTypeAttributeId"],
                    name=fields[attr["objectTypeAttributeId"]].name,
                    ref=fields[attr["objectTypeAttributeId"]].ref,
                    values=[
                        AttrValue(
                            id=val["referencedObject"]["id"] if fields[attr["objectTypeAttributeId"]].ref else None,
                            label=val["displayValue"],
                        )
                        for val in attr["objectAttributeValues"]
                    ],
                )
                for attr in object["attributes"]
            ],
        )

    @classmethod
    @Formatter.key_error_possible
    def decode_update_object(cls, raw_object: dict):
        # переделать прод чистый ретурн
        return InsightObject(
            id=raw_object["id"],
            label=raw_object["label"],
            attrs=[
                ObjectAttr(
                    id=attr["objectTypeAttributeId"],
                    name=attr["objectTypeAttribute"]["name"],
                    ref=attr.get("referenceObjectTypeId", None),
                    values=[
                        AttrValue(
                            id=val["referencedObject"]["id"] if attr.get("referenceObjectTypeId", None) else None,
                            label=val["displayValue"],
                        )
                        for val in attr["objectAttributeValues"]
                    ],
                )
                for attr in raw_object["attributes"]
            ],
        )


class DictionaryFormatter(Formatter):
    @classmethod
    @Formatter.key_error_possible
    def decode_get_object(self, object: dict, fields: dict[int, FieldScheme]) -> dict:
        """Создает человекочитаймый слоарь из JSON ответа, пример ответа:
        https://docs.atlassian.com/assets/REST/9.1.16/#object-createObject"""
        return {
            "link": object["_links"]["self"],
            "id": object["id"],
            **{
                fields.get(attr["objectTypeAttributeId"]).name: DictionaryFormatter._form_attrs(
                    attr["objectAttributeValues"]
                )
                for attr in object["attributes"]
                if fields.get(attr["objectTypeAttributeId"])
            },
        }

    @classmethod
    def _form_attrs(cls, attrs: list) -> Any:
        if len(attrs) == 0:
            return None
        elif len(attrs) == 1:
            return attrs[0]["displayValue"]
        else:
            return [attr["displayValue"] for attr in attrs]

    @classmethod
    def decode_create_object(cls, object: dict):
        raise NotImplementedError()

    @classmethod
    def decode_update_object(cls, object: dict):
        raise NotImplementedError()
