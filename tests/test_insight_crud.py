
import pytest

from services.insight import Insight
from services.schemas import SearchRequest

from .test_connection import client

client = client

@pytest.mark.asyncio
async def test_read(client):
    data = SearchRequest(scheme=10, item_type=155, iql="Key = INT-563705")
    await client.update_token()
    res = await Insight.read(client, data)
    assert isinstance(res, list)
    assert len(res) == 1
    assert res[0].get("objectKey") == "INT-563705"
