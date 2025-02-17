import pytest

from tests.fixtures import get_attr, mars_insight  # noqa


@pytest.mark.mars
@pytest.mark.asyncio(loop_scope="session")
async def test_get_items(mars_insight):  # noqa: F811
    objs = await mars_insight.get_objects(iql="objectId=563705")
    assert isinstance(objs[0], dict)
    assert get_attr(objs[0], "Name")[0]["label"] == "Some test gear"


@pytest.mark.mars
@pytest.mark.asyncio(loop_scope="session")
async def test_get_update_object(mars_insight):  # noqa: F811
    before = (await mars_insight.get_objects(iql="objectId=563705", results=1))[0]
    before_store = get_attr(before, "Store")[0]["label"]
    attrs = {1886: 380820 if before_store == "1014" else 380822}
    after = await mars_insight.update_object(type_id=155, object_id=563705, attrs=attrs)
    assert isinstance(after, dict)
    assert before["id"] == after["id"]
    assert before_store != get_attr(after, "Store")[0]["label"]


@pytest.mark.skip(reason="Нет удаления")
@pytest.mark.asyncio(loop_scope="session")
async def test_get_create_object(mars_insight):  # noqa: F811
    attrs = {1649: "the test creation#12345", 1890: 381686, 1886: 380822, 1891: 382769, 1892: 383219, 1893: 381031}
    obj = await mars_insight.create_object(type_id=155, attrs=attrs)
    assert isinstance(obj, dict)
    assert obj["label"] == "the test creation"
