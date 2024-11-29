import pytest

from services.connection import Client
from services.insight import Insight
from services.schemas import GetObjectData
from tests.fixtures import client  # noqa: F401


@pytest.mark.asyncio
async def test_get_item(client: Client):
    obj = GetObjectData(scheme=10, object_id=563705)
    obj = await Insight.get_object(client, data=obj)
    assert isinstance(obj, dict)
    assert obj["id"] == 563705
