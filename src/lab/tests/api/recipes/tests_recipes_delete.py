import pytest

from lab.models import Recipe

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def recipe(mixer):
    return mixer.blend("lab.Recipe", name="what", sand_weight=10.5)


base_url = "/api/v1/lab/recipes/"


def test_delete(api, recipe):
    api.delete(f"{base_url}{recipe.id}/")

    with pytest.raises(Recipe.DoesNotExist):
        recipe.r()
