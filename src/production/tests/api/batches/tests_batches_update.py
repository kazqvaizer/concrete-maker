from decimal import Decimal

import pytest

pytestmark = [
    pytest.mark.django_db,
]

base_url = "/api/v1/production/batches/"


@pytest.fixture
def batch(mixer, recipe):
    return mixer.blend("production.Batch", recipe=recipe, volume=2.2, sand_weight=10.5)


@pytest.fixture
def ya_recipe(mixer, recipe):
    return mixer.blend("lab.Recipe", recipe=recipe)


def test_update_response(api, batch, ya_recipe):
    got = api.patch(
        f"{base_url}{batch.id}/",
        data={
            "recipe": ya_recipe.id,
            "volume": "2.0",
            "sand_weight": "0",
            "cement_weight": "0.2",
            "gravel_weight": "10",
            "water_weight": "20",
            "admixture_weight": "23.112",
        },
    )

    assert got["id"] == batch.id
    assert got["recipe"] == ya_recipe.id
    assert got["volume"] == "2.000"
    assert got["sand_weight"] == "0.000"
    assert got["cement_weight"] == "0.200"
    assert got["gravel_weight"] == "10.000"
    assert got["water_weight"] == "20.000"
    assert got["admixture_weight"] == "23.112"


def test_actually_stored(api, batch, ya_recipe):
    api.patch(
        f"{base_url}{batch.id}/",
        data={
            "recipe": ya_recipe.id,
            "volume": "2.0",
            "sand_weight": "0",
            "cement_weight": "0.2",
            "gravel_weight": "10",
            "water_weight": "20",
            "admixture_weight": "23.112",
        },
    )

    batch.r()
    assert batch.recipe == ya_recipe
    assert batch.volume == 2
    assert batch.sand_weight == 0
    assert batch.cement_weight == Decimal("0.2")
    assert batch.gravel_weight == 10
    assert batch.water_weight == 20
    assert batch.admixture_weight == Decimal("23.112")


def test_values_not_from_request_are_skipped_on_update(api, batch, recipe):
    api.patch(
        f"{base_url}{batch.id}/",
        data={
            "water_weight": "20",
        },
    )

    batch.r()
    assert batch.recipe == recipe
    assert batch.volume == Decimal("2.2")
    assert batch.sand_weight == Decimal("10.5")
    assert batch.cement_weight == 0
    assert batch.gravel_weight == 0
    assert batch.water_weight == 20
    assert batch.admixture_weight == 0


def test_ignore_id_in_request(api, batch):
    api.patch(
        f"{base_url}{batch.id}/",
        data={
            "id": 100500,
            "volume": "2.0",
        },
    )

    batch.r()
    assert batch.id != 100500
    assert batch.volume == 2
