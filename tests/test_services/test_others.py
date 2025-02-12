import pytest

from services.repository_factories import Formatter, Insight, Interface


@pytest.mark.asyncio
async def test_dict_fomatter():
    client = Insight.create(Interface.MARS_INSIGHT, scheme=10, formatter=Formatter.ATTR_IN_DICT)
    objs = await client.get_objects(iql="objectId=563705")
    print(objs)
    assert objs[0]["id"] == 563705
