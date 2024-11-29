import os

import pytest
from dotenv import load_dotenv

from services.connection import Client


@pytest.fixture(scope="session")
def client():
    print(os.getenv("URL"))
    load_dotenv()
    return Client(
            username=os.getenv("NAME",''), 
            password=os.getenv("PWORD", ''), 
            url=os.getenv("URL", ''),
            client_id=os.getenv("CLIENT_ID", ''), 
            auth_token=os.getenv("TOKEN", ''),
            )
