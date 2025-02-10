from enum import Enum
from os import getenv

from services.connections.inner import MarsClient, WebHooksClient
from services.insight_repository.repository import MetroRepository


class Interface(Enum):
    MARS = MarsClient(
        url=getenv("INSIGHT_MARS_URL", ""),
        username=getenv("INSIGHT_MARS_USERNAME", ""),
        password=getenv("INSIGHT_MARS_PASSWORD", ""),
        client_id=getenv("INSIGHT_MARS_CLIENT_ID", ""),
        auth_token=getenv("INSIGHT_MARS_TOKEN", ""),
    )
    WEB_HOOKS = WebHooksClient(
        url=getenv("INSIGHT_HOOKS_URL", ""),
        username=getenv("WEBHOOK_USERNAME", ""),
        password=getenv("WEBHOOK_PASSWORD", ""),
        client_id=getenv("INSIGHT_MARS_CLIENT_ID", ""),
    )


class Insight:
    @staticmethod
    def create(interface: Interface, scheme: int) -> MetroRepository:
        if interface in {Interface.MARS, Interface.WEB_HOOKS}:
            return MetroRepository(interface.value, scheme)
        raise NotImplementedError()
