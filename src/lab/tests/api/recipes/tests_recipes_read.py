import pytest

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def recipe(mixer):
    return mixer.blend("lab.Recipe", name="what", sand_weight=10.5)


base_url = "/api/v1/lab/recipes/"


@pytest.mark.parametrize(
    "get",
    (
        (lambda api, r: api.get(f"{base_url}")[0]),
        (lambda api, r: api.get(f"{base_url}{r.id}/")),
    ),
)
def test_read(api, recipe, get):
    got = get(api, recipe)

    assert got["id"] == recipe.pk
    assert got["name"] == "what"
    assert got["sand_weight"] == "10.500"
    assert got["cement_weight"] == "0.000"
    assert got["gravel_weight"] == "0.000"
    assert got["water_weight"] == "0.000"
    assert got["admixture_weight"] == "0.000"
