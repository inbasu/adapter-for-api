from .connections.api_connection import JiraAPIClient


class Jira:

    @classmethod
    async def get_issues(cls, client: JiraAPIClient, params: dict[str, str]) -> list[dict]:
        result = await client.get("search/", params=params)        
        return result.json().get("issues", [])



    @classmethod
    async def create_issue(cls, client: JiraAPIClient, project: int,  issue_type: str|int, data: dict):
        result = await client.post('issue/')
        json = {
                "fields": {
                    "issuetype": issue_type,
                    "project": {"id": project},
                    **cls.form_create_fields(data),
                    }
                }

    @classmethod
    async def add_label(cls):
        pass

    @classmethod
    async def add_component(cls):
        pass

    @classmethod
    async def add_comment(cls):
        pass

    @classmethod
    async def add_attachment(cls):
        pass


    @classmethod
    def form_create_fields(cls, data: dict) -> dict:
        result = {}
        # expect only one value
        for field, value in data.items:
            pass
        return result

