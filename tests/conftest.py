import pytest

@pytest.fixture
def system():
    return lambda x: x[::-1]

@pytest.fixture
def inputs():
    return ["alpha", "beta", "gamma"]
