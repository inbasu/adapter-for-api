import json
from dataclasses import dataclass
from os import getenv
from typing import Callable

from aiohttp import ClientSession
from dotenv import load_dotenv


class ClientCredentialsError(Exception):
    pass



class Handler:

    @staticmethod
    def status_code(func) -> Callable:
        async def wrapper(self, url:str, *args, **kwargs) -> Responce:
            resp = await func(self, url, *args, **kwargs)
            match resp.status_code:
                case 200:
                    return resp
                case 401:
                    await self.update_token()
                    return await func(self, url, *args, **kwargs)
            return Responce(resp.status_code, "")
        return wrapper
        

@dataclass
class Responce:
    status_code: int
    data: str
    
    def json(self) -> dict:
        return json.loads(json.loads(self.data).get("result", {}))

class Client:
    def __init__(self, url: str, username: str, password: str, auth_token:str, client_id: str)-> None:
        self._session: ClientSession | None = None
        self._token: str | None = None
        self.url = url
        self.client_id = client_id
        self._auth_header = {"Authorization": f"Basic {auth_token}"}
        self._auth_params = {
                "grant_type": "password",
                "username": username,
                "password": password,
                }

    @property
    def session(self) -> ClientSession:
        if not self._session:
            self._session = ClientSession(base_url=self.url)
        return self._session
    

    async def close(self) -> None:
        if self._session:
            await self._session.close()


    async def update_token(self) -> None:
        async with self.session.get("/uaa/oauth/token", params=self._auth_params, headers=self._auth_header) as resp:
            json_resp = await resp.json()
            self._token = json_resp.get("access_token", "")


    @Handler.status_code
    async def post(self, url: str, data: dict) -> Responce:
        header = {"Authorization": f"Bearer {self._token}"}
        async with self.session.post(url, json={"client_id": self.client_id, **data}, headers=header) as resp:
            print(resp.status)
            return Responce(status_code=resp.status, data=await resp.text())


    @classmethod
    def new(cls, url: str, username: str, password: str, auth_token: str, client_id: str) -> "Client":
        if not all([url, username, password, auth_token, client_id]):
            raise ClientCredentialsError 
        return cls(url, username, password, auth_token, client_id)




load_dotenv()
client = Client.new(
            username=getenv("NAME",''), 
            password=getenv("PWORD", ''), 
            url=getenv("URL", ''),
            client_id=getenv("CLIENT_ID", ''), 
            auth_token=getenv("TOKEN", ''),
            )

