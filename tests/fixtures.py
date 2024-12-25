import os

import pytest
from dotenv import load_dotenv

from services.connections.jira_api_connection import JiraAPIClient
from services.connections.mars_connection import MarsClient


@pytest.fixture(scope="session")
def insight_mars_client():
    load_dotenv()
    return MarsClient(
            username=os.getenv("INSIGHT_MARS_USERNAME",''), 
            password=os.getenv("INSIGHT_MARS_PASSWORD", ''), 
            client_id=os.getenv("INSIGHT_MARS_CLIENT_ID", ''), 
            auth_token=os.getenv("INSIGHT_MARS_TOKEN", ''),
            )


@pytest.fixture(scope="session")
def jira_mars_client():
    load_dotenv()
    return MarsClient(
            username=os.getenv("JIRA_MARS_USERNAME",''), 
            password=os.getenv("JIRA_MARS_PASSWORD", ''), 
            client_id=os.getenv("JIRA_MARS_CLIENT_ID", ''), 
            auth_token=os.getenv("JIRA_MARS_TOKEN", ''), 
            )


@pytest.fixture(scope="session")
def jira_api_client():
    load_dotenv()
    return JiraAPIClient(
            username=os.getenv("JIRA_USER_NAME",''), 
            password=os.getenv("JIRA_PWORD", ''), 
            )
