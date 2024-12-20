from .connections.api_connection import JiraAPIClient
from .schemas import Issue


class Jira:

    @classmethod
    async def get_issues(cls, client: JiraAPIClient, params: dict[str, str]) -> list[Issue]:
        result = await client.get("search/", params=params)        
        print(result)
        return result
