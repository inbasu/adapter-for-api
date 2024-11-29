import pytest

from services.connection import Client
from services.insight import Insight
from services.schemas import FieldScheme, GetObjectData, ObjectResponse
from tests.fixtures import client  # noqa: F401


@pytest.mark.asyncio(loop_scope="session")
async def test_get_item(client: Client):
    obj = await Insight.get_object(client, data= GetObjectData(scheme=10, object_id=563705))
    assert isinstance(obj, ObjectResponse)
    assert obj.id == 563705
    assert obj.attrs

@pytest.mark.asyncio(loop_scope="session")
async def test_get_object_fields(client: Client):
    obj = GetObjectData(scheme=10, object_id=155)
    fields = await Insight.get_object_fields(client, obj)
    assert isinstance(fields, list)
    assert isinstance(fields[0], FieldScheme)
