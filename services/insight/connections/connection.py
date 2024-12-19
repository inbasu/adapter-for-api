import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

from aiohttp import ClientSession


class ClientCredentialsError(Exception):
    pass

@dataclass
class Responce:
    status_code: int
    data: str
    
    def json(self) -> dict:
        return json.loads(json.loads(self.data).get("result", {}))



class InsightClient(ABC):
    
    _session: ClientSession | None = None
    url: str

    @property
    def session(self) -> ClientSession:
        if not self._session:
            self._session = ClientSession(base_url=self.url)
        return self._session


    async def close(self) -> None:
        if self._session:
            await self._session.close()


    @abstractmethod
    async def post(self, url: str, data: dict, content_type: str) -> Responce:
        pass


