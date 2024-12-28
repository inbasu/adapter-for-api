

from services.connections.connection import Client

from .utils import Handler, Responce


class MarsClient(Client):

    def __init__(self, url: str, username: str, password: str, auth_token:str, client_id: str)-> None:
        super().__init__(url, username, password, auth_token, client_id)
        self.url = url
        self._token: str | None = None
        self.client_id = client_id
        self._auth_header = {"Authorization": f"Basic {auth_token}"}
        self._auth_params = {
                "grant_type": "password",
                "username": username,
                "password": password,
                }


    async def update_token(self) -> None:
        resp = await self.session.get("/uaa/oauth/token", params=self._auth_params, headers=self._auth_header)
        json_resp = resp.json()
        self._token = json_resp.get("access_token", "")


    @Handler.status_code
    async def post(self, url: str, data: dict, content_type="application/json") -> Responce:
        headers = {"Content-Type": content_type, "Authorization": f"Bearer {self._token}"}
        resp = await self.session.post(f'{url}', json={"client_id": self.client_id, **data}, headers=headers)
        return Responce(status_code=resp.status_code, data=resp.text)



