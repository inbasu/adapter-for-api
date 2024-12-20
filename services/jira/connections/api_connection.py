from aiohttp import BasicAuth

from services.jira.connections.connection import JiraClient, Responce


class JiraAPIClient(JiraClient):
    url = 'http://jira.metro-cc.ru/rest/api/2/'
    
    def __init__(self, username: str, password: str) -> None:
        self._auth = BasicAuth(username, password)


    async def get(self, url: str, params: dict) -> Responce:
        async with self.session.get(url=url, params=params, auth=self._auth) as resp:
            return Responce(resp.status, await resp.text())
