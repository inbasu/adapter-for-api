

import pytest

from services.connections.mars_connection import MarsClient
from services.jira import Jira
from tests.fixtures import jira_mars_client as client  # noqa: F401


@pytest.mark.asyncio(loop_scope="session")
async def test_create_issue(client: MarsClient):
    obj = await Jira.create_issue(client, project="it", issue="IT-797793", comment="Hello test comment") 
    print(obj)



# @pytest.mark.asyncio(loop_scope="session")
# async def test_add_attach(client: MarsClient):
#     with open("tests/test_services/e.jpeg", "rb") as f:
#         a = base64.b64encode(f.read()).decode("utf-8")
#         obj = await Jira.add_attachment(client, AddAttachment(project="it", issue="IT-797793", source=a, name="e.jpeg")) 
#         assert not obj['error']
# 


