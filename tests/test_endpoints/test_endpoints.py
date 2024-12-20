import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio(loop_scope="session")
async def test_get_object():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        resp = await client.post('/get', json={"scheme": 10, "object_id": 563705})
        assert resp.status_code == 200
        assert resp.json()["id"] == 563705


@pytest.mark.asyncio(loop_scope="session")
async def test_get_objects():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        resp = await client.post('/iql', json={"scheme": 10, "iql": "Name like !test"})
        assert resp.status_code == 200
        assert len(resp.json()) > 10

@pytest.mark.asyncio(loop_scope="session")
async def test_get_issues():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        resp = await client.post('/issues', json={"jql": "key=IT-797207"})
        assert resp.status_code == 200
        assert resp.json()[0]["key"] == "IT-797207"

