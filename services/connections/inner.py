from httpx import AsyncClient, BasicAuth

from .base import Client, Response, Singletone


class MarsClient(Client, metaclass=Singletone):
    def __init__(self, url: str, username: str, password: str, auth_token: str, client_id: str) -> None:
        super().__init__(url, username, password, auth_token, client_id)
        self._token: str | None = None
        self._client_id = client_id
        self._auth_header = {"Authorization": f"Basic {auth_token}"}
        self._auth_params = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }

    @property
    def _session(self) -> AsyncClient:
        if not isinstance(self._the_session, AsyncClient):
            return AsyncClient(base_url=self._url)
        return self._the_session

    async def _update_token(self) -> None:
        resp = await self._session.get(
            f"https://{self._url.host}/uaa/oauth/token", params=self._auth_params, headers=self._auth_header
        )
        json_resp = resp.json()
        self._token = json_resp.get("access_token", "")

    async def post(self, url: str, data: dict, content_type="application/json") -> Response:
        headers = {"Content-Type": content_type, "Authorization": f"Bearer {self._token}"}
        resp = await self._session.post(f"{url}", json={"client_id": self._client_id, **data}, headers=headers)
        if resp.status_code == 401:
            await self._update_token()
            headers = {"Content-Type": content_type, "Authorization": f"Bearer {self._token}"}
            resp = await self._session.post(f"{url}", json={"client_id": self._client_id, **data}, headers=headers)
        return Response(resp)


class WebHooksClient(Client):
    def __init__(self, url: str, username: str, password: str, client_id: str) -> None:
        super().__init__(url, username, password, client_id)
        self._client_id = client_id
        self._auth = BasicAuth(username, password)

    @property
    def _session(self) -> AsyncClient:
        if not isinstance(self._the_session, AsyncClient):
            return AsyncClient(base_url=self._url, auth=self._auth)
        return self._the_session

    async def post(self, url: str, data: dict, content_type="application/json") -> Response:
        headers = {"Content-Type": content_type}
        resp = await self._session.post(f"{url}", json={"client_id": self._client_id, **data}, headers=headers)
        return Response(resp)
