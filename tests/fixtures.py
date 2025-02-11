import pytest

from services.insight import Insight, Interface
from services.insight_repository.repository import MetroRepository


@pytest.fixture(scope="session")
def mars_insight() -> MetroRepository:
    return Insight.create(Interface.MARS, scheme=10)


@pytest.fixture(scope="session")
def web_hooks_insight() -> MetroRepository:
    return Insight.create(Interface.WEB_HOOKS, scheme=10)
