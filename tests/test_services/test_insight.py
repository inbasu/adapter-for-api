import pytest

from services.insight.connections.mars_connection import InsightMarsClient
from services.insight.insight import Insight
from services.insight.schemas import (FieldScheme, GetObjectData,
                                      InsightObject, UpdateObjectData)
from tests.fixtures import insight_mars_client as client  # noqa: F401


@pytest.mark.asyncio(loop_scope="session")
async def test_get_item(client: InsightMarsClient):
    obj = await Insight.get_object(client, data= GetObjectData(scheme=10, object_id=563705))
    assert isinstance(obj, InsightObject)
    assert obj.id == 563705

    
@pytest.mark.asyncio(loop_scope="session")
async def test_get_object_fields(client: InsightMarsClient):
    obj = GetObjectData(scheme=10, object_id=155)
    fields = await Insight.get_object_fields(client, obj)
    assert isinstance(fields, list)
    assert isinstance(fields[0], FieldScheme)
    assert fields[0].name == "Key"


@pytest.mark.asyncio(loop_scope="session")
async def test_update_object(client: InsightMarsClient):
    reverse_state = {"Working": 383219, "Free": 383223}
    obj = await Insight.get_object(client, data= GetObjectData(scheme=10, object_id=563705))
    data = UpdateObjectData(scheme=10, object_type_id=155, object_id=563705,
                            attrs={1892:[reverse_state[obj.get_field_values("State")[0].label
]]})
    changed = await Insight.update_object(client, data)
    assert obj != changed


