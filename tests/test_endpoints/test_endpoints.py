import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio(loop_scope="session")
async def test_get_object():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        resp = await client.post('/get', json={"scheme": 10, "object_id": 563705})
        assert resp.status_code == 200
        assert resp.json()["id"] == 563705


@pytest.mark.asyncio(loop_scope="session")
async def test_get_objects():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        resp = await client.post('/iql', json={"scheme": 10, "iql": "Name like !test"})
        assert resp.status_code == 200
        assert len(resp.json()) > 10
