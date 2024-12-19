from aiohttp import BasicAuth

from services.insight.connections.connection import InsightClient
from services.insight.connections.utils import Handler, Responce


class InsightAPIClient(InsightClient):
    
    def __init__(self, url:str, username: str, password: str) -> None:
        self.url = url
        self.auth = BasicAuth(username, password)

    @Handler.status_code
    async def post(self, url: str, data: dict, content_type="application/json"):
        headers = {"Content-Type": content_type}
        async with self.session.post(url, data=data,auth=self.auth, headers=headers) as resp:
            return Responce(status_code=resp.status, data=await resp.json())


