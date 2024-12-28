from fastapi import APIRouter

from services.jira import Jira
from services.schemas.jira_schemas import AddAttachment
from settings import jira_api_client, jira_mars_client

jira_router = APIRouter()


@jira_router.post("/issues")
async def get_object(jql: dict[str, str]):
    return await Jira.get_issues(client=jira_api_client, params=jql)


@jira_router.post("/add_attachment")
async def add_attachment(data: AddAttachment):
    return await Jira.add_attachment(client=jira_mars_client, data=data)
