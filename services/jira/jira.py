from .connections.api_connection import JiraAPIClient


class Jira:

    @classmethod
    async def get_issues(cls, client: JiraAPIClient, params: dict[str, str]) -> list[dict]:
        result = await client.get("search/", params=params)        
        return result.json().get("issues", [])



