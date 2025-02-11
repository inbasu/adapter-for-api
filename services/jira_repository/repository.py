from services.connections.base import Client


class JiraMetroRepository:
    """
    #TODO
    1 - create_issue - не все поля доступны и не возможности создать задачу
    2 - get_issues - нет такого эндпоинта
    *3 - update_issue - не все поля доступны для редактировани и пофиг
    4 - comment_issue - говорит что комментит, но не комментит
    """

    def __init__(self, client: Client, project: str) -> None:
        self._client = client
        self._project = project

    """ Issue(s) manipulations """

    async def create_issue(self, summary: str, description: str, fields: dict):
        """Not all fieldsavalible"""
        json = {
            "project": self._project,
            "fields": [
                {"name": "summary", "value": summary},
                {"name": "description", "value": description},
                *[{"name": name, "value": value} for name, value in fields.items()],
            ],
        }
        response = await self._client.post("/issue/run", data=json)

    async def get_issues(self):
        raise NotImplementedError()

    async def update_issue(self, issue: str, fields: dict):
        json = {
            "project": self._project,
            "issue": issue,
            "comment": "",
            "fields": [{"name": name, "value": value} for name, value in fields.items()],
        }
        response = await self._client.post("/update/run", data=json)
        if response.status_code == 200:
            print(response.data)

    """ Comments """

    async def comment_issue(self, issue: str, comment: str, public: bool = True):
        raise NotImplementedError()
        json = {"project": self._project, "issue": issue, "public": public, "comment": comment}
        responce = await self._client.post("/comment/run", data=json)
        if responce.status_code == 200:
            return ""
        return ""

    """ Attachments """

    async def upload_attachment(self, issue: str, file_name: str, file):
        """Add attachment base64"""
        json = {
            "project": self._project,
            "method": "base64",
            "issue": issue,
            "source": {"name": file_name, "link": file},
        }
        response = self._client.post("", data=json)
