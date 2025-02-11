from enum import Enum
from os import getenv

from services.connections.inner import MarsClient, WebHooksClient
from services.insight_repository.repository import InsightMetroRepository
from services.jira_repository.repository import JiraMetroRepository


class Interface(Enum):
    MARS_INSIGHT = MarsClient(
        url=getenv("MARS_URL", ""),
        username=getenv("INSIGHT_MARS_USERNAME", ""),
        password=getenv("INSIGHT_MARS_PASSWORD", ""),
        client_id=getenv("INSIGHT_MARS_CLIENT_ID", ""),
        auth_token=getenv("INSIGHT_MARS_TOKEN", ""),
    )
    WEB_HOOKS_INSIGHT = WebHooksClient(
        url=getenv("INSIGHT_HOOKS_URL", ""),
        username=getenv("WEBHOOK_USERNAME", ""),
        password=getenv("WEBHOOK_PASSWORD", ""),
        client_id=getenv("INSIGHT_MARS_CLIENT_ID", ""),
    )


#    MARS_JIRA = MarsClient(
#        url=getenv("MARS_URL", ""),
#        username=getenv("JIRA_MARS_USERNAME", ""),
#        password=getenv("JIRA_MARS_PASSWORD", ""),
#        client_id=getenv("JITA_MARS_CLIENT_ID", ""),
#        auth_token=getenv("JIRA_MARS_TOKEN", ""),
#    )
#    WEB_HOOKS_JIRA = WebHooksClient(
#        url=getenv("JIRA_HOOKS_URL", ""),
#        username=getenv("WEBHOOK_USERNAME", ""),
#        password=getenv("WEBHOOK_PASSWORD", ""),
#        client_id=getenv("INSIGHT_MARS_CLIENT_ID", ""),
#    )


class Project(Enum):
    IT = "it"
    ITREQ = "itreq"


class Insight:
    @staticmethod
    def create(interface: Interface, scheme: int) -> InsightMetroRepository:
        if interface in {Interface.MARS_INSIGHT, Interface.WEB_HOOKS_INSIGHT}:
            return InsightMetroRepository(interface.value, scheme)
        raise NotImplementedError()


# class Jira:
#    @staticmethod
#    def create(interface, project: Project):
#        if interface in {Interface.MARS_JIRA, Interface.WEB_HOOKS_JIRA}:
#            return JiraMetroRepository(interface.value, project.value)
