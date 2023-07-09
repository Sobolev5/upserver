import os
import pytest
import asyncio


@pytest.fixture(scope="module")
def define_test_scope() -> pytest.fixture():
    os.environ["TEST"] = "1"
    return os.environ["TEST"]


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


