import pytest

from bankaccount.app import create_app
from bankaccount.settings import TestConfig

@pytest.yield_fixture()
def app():
    return create_app(TestConfig)