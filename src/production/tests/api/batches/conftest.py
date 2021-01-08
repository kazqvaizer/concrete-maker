import pytest


@pytest.fixture
def recipe(mixer):
    return mixer.blend("lab.Recipe")
