import pytest

from services.connection import Client
from services.insight import Insight
from services.schemas import (FieldScheme, GetObjectData, ObjectResponse,
                              UpdateObjectData)
from tests.fixtures import client  # noqa: F401


@pytest.mark.asyncio(loop_scope="session")
async def test_get_item(client: Client):
    obj = await Insight.get_object(client, data= GetObjectData(scheme=10, object_id=563705))
    assert isinstance(obj, ObjectResponse)
    assert obj.id == 563705

    
@pytest.mark.asyncio(loop_scope="session")
async def test_get_object_fields(client: Client):
    obj = GetObjectData(scheme=10, object_id=155)
    fields = await Insight.get_object_fields(client, obj)
    assert isinstance(fields, list)
    assert isinstance(fields[0], FieldScheme)
    assert fields[0].name == "Key"


@pytest.mark.asyncio(loop_scope="session")
async def test_update_object(client: Client):
    reverse_state = {"Working": 383219, "Free": 383223}
    obj = await Insight.get_object(client, data= GetObjectData(scheme=10, object_id=563705))
    data = UpdateObjectData(scheme=10, object_type_id=155, object_id=563705,
                            attrs={1892:[reverse_state[obj.get_field_values("State")[0].label
]]})
    changed = await Insight.update_object(client, data)
    assert obj != changed


