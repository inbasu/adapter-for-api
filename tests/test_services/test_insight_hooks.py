import pytest

from services.connections.mars_connection import MarsClient
from services.insight import MetroInsight
from services.schemas.insight_schemas import InsightObject
from tests.fixtures import insight_hooks_client as client  # noqa: F401

""" MARS """


@pytest.mark.web_hooks
@pytest.mark.asyncio(loop_scope="session")
async def test_get_items(client: MarsClient):
    objs = await MetroInsight.get_objects(client, scheme=10, iql="objectId=563705")
    assert isinstance(objs[0], InsightObject)
    assert objs[0].get_field_values("Name")[0].label == "Some test gear"


@pytest.mark.web_hooks
@pytest.mark.asyncio(loop_scope="session")
async def test_get_update_object(client: MarsClient):
    before = (await MetroInsight.get_objects(client, scheme=10, iql="objectId=563705", results=1))[0]
    before_store = before.get_field_values("Store")[0].label
    attrs = {1886: 380820 if before_store == "1014" else 380822}
    after = await MetroInsight.update_object(client, scheme=10, type_id=155, object_id=563705, attrs=attrs)
    assert isinstance(after, InsightObject)
    assert before == after
    assert before_store != after.get_field_values("Store")[0].label


@pytest.mark.skip(reason="Нет удаления")
@pytest.mark.asyncio(loop_scope="session")
async def test_get_create_object(client: MarsClient):
    attrs = {1649: "the test creation#12345", 1890: 381686, 1886: 380822, 1891: 382769, 1892: 383219, 1893: 381031}
    obj = await MetroInsight.create_object(client, scheme=10, type_id=155, attrs=attrs)
    assert isinstance(obj, InsightObject)
    assert obj.label == "the test creation"
