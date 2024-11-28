
import pytest

from database.connection import async_session
from database.repository import EntityUOW
from services.schemas import EntityScheme, Field

from .test_connection import client

client = client

# @pytest.mark.asyncio
# async def test_read(client):
#     data = SearchRequest(scheme=10, item_type=155, iql="Key = INT-563705")
#     await client.update_token()
#     res = await Insight.read(client, data)
#     assert isinstance(res, list)
#     assert len(res) == 1
#     assert res[0].get("objectKey") == "INT-563705"



@pytest.mark.asyncio
async def test_fill_table():
    session = async_session()
    await EntityUOW.create_entity(session, EntityScheme(scheme=1, item_type=1, name="h"), [Field(name="1", id=1)])
    assert await EntityUOW.get_id_with_name(session=session, scheme=1, name="h") == 1
    
