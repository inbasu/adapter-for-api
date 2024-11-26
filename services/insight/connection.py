import json
from dataclasses import dataclass
from typing import Callable

from aiohttp import ClientSession


class StatusCode:

    @classmethod
    def check(cls, func) -> Callable:
        async def wrapper(self, url:str, *args) -> Responce:
            resp = await func(self, url, *args)
            match resp.status_code:
                case 200:
                    return resp
            return Responce(500, "")
        return wrapper



@dataclass
class Responce:
    status_code: int
    data: str

    def json(self) -> dict:
        return json.loads(self.data)



class Client:
    def __init__(self)-> None:
        self._session: ClientSession | None = None

    def get_session(self) -> ClientSession:
        # logging here
        if not self._session:
            self._session = ClientSession()
        return self._session

    
    async def close(self) -> None:
        if self._session:
            await self._session.close()

    async def update_token(self) -> None:
        return None


    @StatusCode.check
    async def get(self, url: str):
        async with self.get_session() as session:
            async with session.get(url) as resp:
                return Responce(status_code=resp.status, data=await resp.text())


    async def post(self, url: str):
        async with self.get_session() as session:
            async with session.post(url) as resp:
                return Responce(status_code=resp.status, data=await resp.text())


        

