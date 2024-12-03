import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.mark.asyncio(loop_scope="session")
async def test_get_object():
    with TestClient(app) as client:
        resp = client.post('/get', json={"scheme": 10, "object_id": 563705})
        assert resp.status_code == 200
        assert resp.json()["id"] == 563705


@pytest.mark.asyncio(loop_scope="session")
async def test_get_objects():
    with TestClient(app) as client:
        resp = client.post('/iql', json={"scheme": 10, "iql": "Name like !test"})
        assert resp.status_code == 200
        assert len(resp.json()) == 59
