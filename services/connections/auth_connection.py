from httpx import AsyncClient, BasicAuth

from services.connections.connection import Client, Response


class MarsClient(Client):
    def __init__(self, url: str, username: str, password: str, client_id: str) -> None:
        super().__init__(url)
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
