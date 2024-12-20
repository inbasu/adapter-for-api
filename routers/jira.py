
from fastapi import APIRouter

from services.jira.jira import Jira
from settings import jira_api_client

jira_router = APIRouter()


@jira_router.post('/issues')
async def get_object(jql):
    return await Jira.get_issues(client=jira_api_client, params={"jql": jql})
