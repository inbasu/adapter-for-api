from services.connections.connection import Client, Responce
from services.connections.utils import Handler


class InsightAPIClient(Client):

    def __init__(self, url: str, username: str, password: str) -> None:
        self.url = url
        self.auth = (username, password)

    @Handler.status_code
    async def post(self, url: str, data: dict, content_type="application/json"):
        headers = {"Content-Type": content_type}
        resp = await self.session.post(url, data=data, auth=self.auth, headers=headers)
        return Responce(status_code=resp.status_code, data=await resp.json())
