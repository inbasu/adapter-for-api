import pytest

from services.insight import Insight, Interface
from services.insight_repository.repository import InsightMetroRepository


@pytest.fixture(scope="session")
def mars_insight() -> InsightMetroRepository:
    return Insight.create(Interface.MARS_INSIGHT, scheme=10)


@pytest.fixture(scope="session")
def web_hooks_insight() -> InsightMetroRepository:
    return Insight.create(Interface.WEB_HOOKS_INSIGHT, scheme=10)
