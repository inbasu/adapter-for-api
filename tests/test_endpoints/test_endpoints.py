
import base64

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
async def test_add_attachment():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        with open("tests/test_services/e.jpeg", "rb") as f:
            a = base64.b64encode(f.read()).decode("utf-8")
        resp = await client.post('/add_attachment', json={"project": "it", "issue": "IT-797793", "name": "e.jpeg", "source": a})
        assert resp.status_code == 200
        assert not resp.json()["error"]
