import os

import dotenv
import pytest

from services.connection import Client

dotenv.load_dotenv()


@pytest.fixture
def client() -> Client:
    return Client(
            username=os.getenv("NAME"), 
            password=os.getenv("PWORD"), 
            url=os.getenv("URL"),
            client_id=os.getenv("CLIENT_ID"), 
            auth_token=os.getenv("TOKEN"),
            )


@pytest.mark.asyncio
async def test_get_token(client):
    assert not client._token
    await client.update_token()
    assert client._token


@pytest.mark.asyncio
async def test_get_item(client):
    resp = await client.post("iql/run", {"scheme": 10, "iql": "Key = INT-563705"})
    print(resp)
