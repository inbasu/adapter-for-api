from .connections.jira_api_connection import JiraAPIClient
from .connections.mars_connection import MarsClient
from .schemas.jira_schemas import AddAttachment


class Jira:

    @classmethod
    async def get_issues(cls, client: JiraAPIClient, params: dict[str, str]) -> list[dict]:
        result = await client.get("search/", params=params)
        return result.json().get("issues", [])

    @classmethod
    async def create_issue(cls, client, data):
        json = {"project": "it"}
        result = await client.post("/ru-jira/issue/run", data=json)
        print(result)

    @classmethod
    async def add_attachment(cls, client: MarsClient, data: AddAttachment):
        json = {
            "project": data.project,
            "issue": data.issue,
            "method": "base64",
            "source": [{"name": data.name, "link": data.source}],
        }
        result = await client.post("/ru-jira/attachment/run", data=json)
        return result.json()

    @classmethod
    async def comment_issue(cls, client: MarsClient, project: str, issue: str, comment: str, public: bool = True):
        json = {"project": project, "issue": issue, "comment": comment, "public": "true"}
        result = await client.post("/ru-jira/comment/run", data=json)
        print(result)

    @classmethod
    def form_fields(cls, data: dict) -> list[dict]:
        return [{"name": key, "value": value} for key, value in data.items()]
