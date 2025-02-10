import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

from httpx import URL, AsyncClient
from httpx import Response as R


class ClientCredentialsError(Exception):
    pass


class Response:
    def __init__(self, response: R) -> None:
        self.status_code = response.status_code
        self.data = self._form_data(response)

    def _form_data(self, response) -> dict:
        if response.status_code == 200:
            try:
                return json.loads(response.json().get("result"))
            except json.JSONDecodeError:
                return json.loads(response.text)
        return response.json()


class Client(ABC):
    def __init__(self, url: str, *args, **kwargs):
        if not all(args):
            raise ClientCredentialsError("Присутствуют аргументы с нулеым значением, проверьте .env")
        self._url = URL(url)
        self._the_session: AsyncClient | None = None

    @property
    @abstractmethod
    def _session(self) -> AsyncClient:
        pass

    async def close(self) -> None:
        if self._the_session:
            await self._session.aclose()

    @abstractmethod
    async def post(self, url: str, data: dict, content_type: str = "application/json") -> Response:
        pass
