from enum import Enum
from os import getenv

from dotenv import load_dotenv

from services.connections.inner import MarsClient, WebHooksClient
from services.insight_repository.formatters import DefaultAssetToolFormatter, DictionaryFormatter
from services.insight_repository.repository import InsightMetroUnit
from services.jira_repository.repository import JiraMetroUnit


class Formatter(Enum):
    ATTRS_IN_LIST = DefaultAssetToolFormatter
    ATTR_IN_DICT = DictionaryFormatter


class Interface(Enum):
    """
    Загрузка кредлов
    """

    load_dotenv()
    MARS_INSIGHT = dict(
        url=getenv("INSIGHT_MARS_URL", ""),
        username=getenv("INSIGHT_MARS_USERNAME", ""),
        password=getenv("INSIGHT_MARS_PASSWORD", ""),
        client_id=getenv("INSIGHT_MARS_CLIENT_ID", ""),
        auth_token=getenv("INSIGHT_MARS_TOKEN", ""),
    )
    WEB_HOOKS_INSIGHT = dict(
        url=getenv("INSIGHT_HOOKS_URL", ""),
        username=getenv("WEBHOOK_USERNAME", ""),
        password=getenv("WEBHOOK_PASSWORD", ""),
        client_id=getenv("INSIGHT_MARS_CLIENT_ID", ""),
    )

    MARS_JIRA = dict(
        url=getenv("JIRA_MARS_URL", ""),
        username=getenv("JIRA_MARS_USERNAME", ""),
        password=getenv("JIRA_MARS_PASSWORD", ""),
        client_id=getenv("JIRA_MARS_CLIENT_ID", ""),
        auth_token=getenv("JIRA_MARS_TOKEN", ""),
    )
    WEB_HOOKS_JIRA = dict(
        url=getenv("JIRA_HOOKS_URL", ""),
        username=getenv("WEBHOOK_USERNAME", ""),
        password=getenv("WEBHOOK_PASSWORD", ""),
        client_id=getenv("INSIGHT_MARS_CLIENT_ID", ""),
    )


class Project(Enum):
    IT = ("it", 1)
    ITREQ = ("it", 3448)


class Insight:
    @staticmethod
    def create(interface: Interface, scheme: int, formatter: Formatter) -> InsightMetroUnit:
        match interface:
            case Interface.MARS_INSIGHT:
                return InsightMetroUnit(MarsClient(**interface.value), scheme, formatter.value)
            case Interface.WEB_HOOKS_INSIGHT:
                return InsightMetroUnit(WebHooksClient(**interface.value), scheme, formatter.value)
        raise NotImplementedError()


class Jira:
    @staticmethod
    def create(interface, project: Project) -> JiraMetroUnit:
        match interface:
            case Interface.MARS_JIRA:
                return JiraMetroUnit(MarsClient(**interface.value), project.value[0], project.value[1])
            case Interface.WEB_HOOKS_JIRA:
                return JiraMetroUnit(WebHooksClient(**interface.value), project.value[0], project.value[1])
        raise NotImplementedError()
