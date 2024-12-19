

from services.insight.connections.connection import InsightClient

from .utils import Handler, Responce


class InsightMarsClient(InsightClient):
    url = "https://api.metronom.dev/ru-insight/"

    def __init__(self, username: str, password: str, auth_token:str, client_id: str)-> None:
        self._token: str | None = None
        self.client_id = client_id
        self._auth_header = {"Authorization": f"Basic {auth_token}"}
        self._auth_params = {
                "grant_type": "password",
                "username": username,
                "password": password,
                }


    async def update_token(self) -> None:
        async with self.session.get("/uaa/oauth/token", params=self._auth_params, headers=self._auth_header) as resp:
            json_resp = await resp.json()
            self._token = json_resp.get("access_token", "")


    @Handler.status_code
    async def post(self, url: str, data: dict, content_type="application/json") -> Responce:
        headers = {"Content-Type": content_type, "Authorization": f"Bearer {self._token}"}
        async with self.session.post(url, json={"client_id": self.client_id, **data}, headers=headers) as resp:
            return Responce(status_code=resp.status, data=await resp.text())


