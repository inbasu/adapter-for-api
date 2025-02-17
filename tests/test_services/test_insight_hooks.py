import pytest

from tests.fixtures import get_attr, web_hooks_insight  # noqa: F401


@pytest.mark.web_hooks
@pytest.mark.asyncio(loop_scope="session")
async def test_get_items(web_hooks_insight):  # noqa
    objs = await web_hooks_insight.get_objects(iql="objectId=563705")
    assert isinstance(objs[0], dict)
    assert objs[0].get_field("Name", [{}])[0].label == "Some test gear"


@pytest.mark.web_hooks
@pytest.mark.asyncio(loop_scope="session")
async def test_get_update_object(web_hooks_insight):  # noqa
    before = (await web_hooks_insight.get_objects(iql="objectId=563705", results=1))[0]
    before_store = before.get_field_values("Store")[0].label
    attrs = {1886: 380820 if before_store == "1014" else 380822}
    after = await web_hooks_insight.update_object(type_id=155, object_id=563705, attrs=attrs)
    assert isinstance(after, dict)
    assert before == after
    assert before_store != after.get("Store", [{}])[0]["label"]


@pytest.mark.skip(reason="Нет удаления")
@pytest.mark.asyncio(loop_scope="session")
async def test_get_create_object(web_hooks_insight):  # noqa
    attrs = {1649: "the test creation#12345", 1890: 381686, 1886: 380822, 1891: 382769, 1892: 383219, 1893: 381031}
    obj = await web_hooks_insight.create_object(type_id=150, attrs=attrs)
    assert isinstance(obj, dict)
    assert obj["label"] == "the test creation"
