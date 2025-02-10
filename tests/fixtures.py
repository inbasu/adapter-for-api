import os

import pytest
from dotenv import load_dotenv

from services.connections.auth_connection import WebHooksClient
from services.connections.mars_connection import MarsClient


@pytest.fixture(scope="session")
def insight_mars_client():
    load_dotenv()
    return MarsClient(
        url=os.getenv("MARS_URL", ""),
        username=os.getenv("INSIGHT_MARS_USERNAME", ""),
        password=os.getenv("INSIGHT_MARS_PASSWORD", ""),
        client_id=os.getenv("INSIGHT_MARS_CLIENT_ID", ""),
        auth_token=os.getenv("INSIGHT_MARS_TOKEN", ""),
    )


@pytest.fixture(scope="session")
def insight_hooks_client():
    load_dotenv()
    return WebHooksClient(
        url=os.getenv("MARS_URL", ""),
        client_id=os.getenv("INSIGHT_MARS_CLIENT_ID", ""),
        username=os.getenv("ASSET_USER_NAME", ""),
        password=os.getenv("ASSET_PASSWORD", ""),
    )
