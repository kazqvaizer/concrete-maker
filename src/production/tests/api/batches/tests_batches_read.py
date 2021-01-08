import pytest

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def batch(mixer, recipe):
    return mixer.blend("production.Batch", recipe=recipe, volume=2.2, sand_weight=10.5)


base_url = "/api/v1/production/batches/"


@pytest.mark.parametrize(
    "get",
    (
        (lambda api, r: api.get(f"{base_url}")[0]),
        (lambda api, r: api.get(f"{base_url}{r.id}/")),
    ),
)
def test_read(api, batch, recipe, get):
    got = get(api, batch)

    assert got["id"] == batch.pk
    assert got["recipe"] == recipe.pk
    assert got["volume"] == "2.200"
    assert got["sand_weight"] == "10.500"
    assert got["cement_weight"] == "0.000"
    assert got["gravel_weight"] == "0.000"
    assert got["water_weight"] == "0.000"
    assert got["admixture_weight"] == "0.000"
