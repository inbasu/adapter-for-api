import pytest

from services.insight.connection import Client, Responce


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.mark.asyncio
async def test_200_connection(client):
    resp = await client.get(url="https://duckduckgo.com/")
    assert resp.__class__ == Responce
    await client.close() # <- create fixture    
