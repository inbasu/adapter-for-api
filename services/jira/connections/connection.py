import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

from httpx import AsyncClient


class ClientCredentialsError(Exception):
    pass

@dataclass
class Responce:
    status_code: int
    data: str | dict | list
    
    def json(self) -> dict | list:
        if isinstance(self.data, str):
            return json.loads(json.loads(self.data).get("result", {}))
        return self.data


class JiraClient(ABC):
    
    _session: AsyncClient | None = None
    url: str

    @property
    def session(self) -> AsyncClient:
        if not self._session:
            self._session = AsyncClient(base_url=self.url)
        return self._session


    async def close(self) -> None:
        if self._session:
            await self._session.aclose()



    @abstractmethod
    async def get(self, url: str, params: dict) -> Responce:
        pass
