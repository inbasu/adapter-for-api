import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

from httpx import AsyncClient


class ClientCredentialsError(Exception):
    pass

@dataclass
class Responce:
    status_code: int
    data: str
    
    def json(self):
        try:
            return json.loads(json.loads(self.data).get("result", {}))
        except json.JSONDecodeError:
            return json.loads(self.data)



class Client(ABC):
    
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
    async def post(self, url: str, data: dict, content_type: str) -> Responce:
        pass



