import os

import pytest
from dotenv import load_dotenv

from services.insight.connections.mars_connection import InsightMarsClient
from services.jira.connections.api_connection import JiraAPIClient


@pytest.fixture(scope="session")
def insight_mars_client():
    load_dotenv()
    return InsightMarsClient(
            username=os.getenv("NAME",''), 
            password=os.getenv("PWORD", ''), 
            client_id=os.getenv("CLIENT_ID", ''), 
            auth_token=os.getenv("TOKEN", ''),
            )



@pytest.fixture(scope="session")
def jira_api_client():
    load_dotenv()
    return JiraAPIClient(
            username=os.getenv("JIRA_USER_NAME",''), 
            password=os.getenv("JIRA_PWORD", ''), 
            )
