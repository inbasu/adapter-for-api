import os

import dotenv
import pytest

from services.connection import Client

dotenv.load_dotenv()


@pytest.fixture
def client() -> Client:
    return Client(
            username=os.getenv("USERNAME"), 
            password=("PASSWORD"), 
            url=os.getenv("URL"),
            client_id=os.getenv("CLIENT_ID"), 
            auth_token=os.getenv("TOKEN"),
            )


@pytest.mark.asyncio
async def test_get_token(client):
    await client.update_token()
    print(client._token)
    await client.close() # <- create fixture    
