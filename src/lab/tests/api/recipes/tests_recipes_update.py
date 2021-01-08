from decimal import Decimal

import pytest

pytestmark = [
    pytest.mark.django_db,
]

base_url = "/api/v1/lab/recipes/"


@pytest.fixture
def recipe(mixer):
    return mixer.blend("lab.Recipe", name="what", sand_weight=10.5)


def test_update_response(api, recipe):
    got = api.patch(
        f"{base_url}{recipe.id}/",
        data={
            "name": "hey",
            "sand_weight": "0",
            "cement_weight": "0.2",
            "gravel_weight": "10",
            "water_weight": "20",
            "admixture_weight": "23.112",
        },
    )

    assert got["id"] == recipe.id
    assert got["name"] == "hey"
    assert got["sand_weight"] == "0.000"
    assert got["cement_weight"] == "0.200"
    assert got["gravel_weight"] == "10.000"
    assert got["water_weight"] == "20.000"
    assert got["admixture_weight"] == "23.112"


def test_actually_stored(api, recipe):
    api.patch(
        f"{base_url}{recipe.id}/",
        data={
            "name": "hey",
            "sand_weight": "0",
            "cement_weight": "0.2",
            "gravel_weight": "10",
            "water_weight": "20",
            "admixture_weight": "23.112",
        },
    )

    recipe.r()
    assert recipe.name == "hey"
    assert recipe.sand_weight == 0
    assert recipe.cement_weight == Decimal("0.2")
    assert recipe.gravel_weight == 10
    assert recipe.water_weight == 20
    assert recipe.admixture_weight == Decimal("23.112")


def test_values_not_from_request_are_skipped_on_update(api, recipe):
    api.patch(
        f"{base_url}{recipe.id}/",
        data={
            "water_weight": "20",
        },
    )

    recipe.r()
    assert recipe.name == "what"
    assert recipe.sand_weight == Decimal("10.5")
    assert recipe.cement_weight == 0
    assert recipe.gravel_weight == 0
    assert recipe.water_weight == 20
    assert recipe.admixture_weight == 0


def test_ignore_id_in_request(api, recipe):
    api.patch(
        f"{base_url}{recipe.id}/",
        data={
            "id": 100500,
            "name": "Yes!",
        },
    )

    recipe.r()
    assert recipe.id != 100500
    assert recipe.name == "Yes!"
