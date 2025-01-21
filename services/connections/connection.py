import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

from httpx import AsyncClient, Timeout


class ClientCredentialsError(Exception):
    pass


@dataclass
class Responce:
    status_code: int
    data: str

    def json(self):
        try:
            # Try пробует обрабоать респонс, как будто это MARS респонс!
            return json.loads(json.loads(self.data).get("result", {}))
        except KeyError:
            return {}
        except json.JSONDecodeError:
            return json.loads(self.data)


class Client(ABC):

    def __init__(self, *args, **kwargs):
        if not all(args):
            raise ClientCredentialsError("Присутствуют аргументы с нулеым значением, проверьте .env")

    _session: AsyncClient | None = None
    url: str

    @property
    def session(self) -> AsyncClient:
        if not self._session:
            self._session = AsyncClient(base_url=self.url, timeout=Timeout(10, read=None))
        return self._session

    async def close(self) -> None:
        if self._session:
            await self._session.aclose()

    @abstractmethod
    async def post(self, url: str, data: dict, content_type: str) -> Responce:
        pass
