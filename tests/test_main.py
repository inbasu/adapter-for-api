import os

import pytest
from dotenv import find_dotenv, load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env():
    print("__")
    env = find_dotenv(".env")
    load_dotenv(env)
