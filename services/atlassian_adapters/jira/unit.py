from services.atlassian_adapters.connections.base import Client


class JiraMetroUnit:
    """
    #TODO
    1 - create_issue - не все поля доступны и не возможности создать задачу
    2 - get_issues - нет такого эндпоинта
    *3 - update_issue - не все поля доступны для редактировани и пофиг
    4 - comment_issue - говорит что комментит, но не комментит
    """

    def __init__(self, client: Client, project: str, request_type: int) -> None:
        self._client = client
        self.project = project
        self._request_type = request_type

    """ Issue(s) manipulations """

    async def create_issue(self, summary: str, description: str, fields: dict):
        """Not all fieldsavalible"""
        json = {
            "project": self.project,
            "type": self._request_type,
            "fields": [
                {"name": "summary", "value": summary},
                {"name": "description", "value": description},
                *[{"name": name, "value": value} for name, value in fields.items()],
            ],
        }
        response = await self._client.post("/issue/run", data=json)
        return response.data.get("result", None)

    async def get_issues(self, jql: str):
        raise NotImplementedError()

    async def update_issue(self, issue: str, fields: dict):
        json = {
            "project": self.project,
            "issue": issue,
            "comment": "",
            "fields": [{"name": name, "value": value} for name, value in fields.items()],
        }
        response = await self._client.post("/update/run", data=json)
        return response.status_code == 200

    """ Comments """

    async def comment_issue(self, issue: str, comment: str, public: bool = True):
        json = {"project": self.project, "issue": issue, "public": public, "comment": comment}
        response = await self._client.post("/comment/run", data=json)
        return response.status_code == 200

    """ Attachments """

    async def upload_attachment(self, issue: str, file_name: str, file: str):
        """Add attachment base64"""
        json = {
            "project": self.project,
            "method": "base64",
            "issue": issue,
            "source": [{"name": file_name, "link": file}],
        }
        response = await self._client.post("/attachment/run", data=json)
        print(response.status_code)
        # return response.status_code == 200
