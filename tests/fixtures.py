import pytest

from services.insight_repository.repository import InsightMetroUnit
from services.jira_repository.repository import JiraMetroUnit
from services.repository_factories import Formatter, Insight, Interface, Jira, Project


@pytest.fixture(scope="session")
def mars_insight() -> InsightMetroUnit:
    return Insight.create(Interface.MARS_INSIGHT, scheme=10, formatter=Formatter.ATTRS_IN_LIST)


@pytest.fixture(scope="session")
def web_hooks_insight() -> InsightMetroUnit:
    return Insight.create(Interface.WEB_HOOKS_INSIGHT, scheme=10, formatter=Formatter.ATTRS_IN_LIST)


@pytest.fixture(scope="session")
def mars_jira() -> JiraMetroUnit:
    return Jira.create(Interface.MARS_JIRA, Project.ITREQ)
