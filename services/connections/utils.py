from typing import Callable

from .connection import Responce


class Handler:

    @staticmethod
    def status_code(func) -> Callable:
        async def wrapper(self, url: str, *args, **kwargs) -> Responce:
            resp = await func(self, url, *args, **kwargs)
            match resp.status_code:
                case 200:
                    return resp
                case 401:
                    await self.update_token()
                    return await func(self, url, *args, **kwargs)
            return Responce(resp.status_code, "")

        return wrapper
