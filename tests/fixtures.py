import pytest

from services.atlassian_adapters.insight.unit import InsightMetroUnit
from services.atlassian_adapters.jira.unit import JiraMetroUnit
from services.atlassian_adapters.unit_factory import Formatter, Insight, Interface, Jira, Project


@pytest.fixture(scope="session")
def mars_insight() -> InsightMetroUnit:
    return Insight.create(Interface.MARS_INSIGHT, scheme=10, formatter=Formatter.ATTRS_IN_LIST)


@pytest.fixture(scope="session")
def web_hooks_insight() -> InsightMetroUnit:
    return Insight.create(Interface.WEB_HOOKS_INSIGHT, scheme=10, formatter=Formatter.ATTRS_IN_LIST)


@pytest.fixture(scope="session")
def mars_jira() -> JiraMetroUnit:
    return Jira.create(Interface.MARS_JIRA, Project.ITREQ)


def get_attr(data: dict, field: str) -> list:
    for attr in data.get("attrs", [{}]):
        if attr["name"] == field:
            return attr["values"]
    return []
