from decimal import Decimal

import pytest

from lab.models import Recipe

pytestmark = [
    pytest.mark.django_db,
]

base_url = "/api/v1/lab/recipes/"


def test_add_response(api):
    got = api.post(
        f"{base_url}",
        data={
            "name": "hey",
            "sand_weight": "0",
            "cement_weight": "0.2",
            "gravel_weight": "10",
            "water_weight": "20",
            "admixture_weight": "23.112",
        },
    )

    assert "id" in got
    assert got["name"] == "hey"
    assert got["sand_weight"] == "0.000"
    assert got["cement_weight"] == "0.200"
    assert got["gravel_weight"] == "10.000"
    assert got["water_weight"] == "20.000"
    assert got["admixture_weight"] == "23.112"


def test_actually_stored(api):
    got = api.post(
        f"{base_url}",
        data={
            "name": "hey",
            "sand_weight": "0",
            "cement_weight": "0.2",
            "gravel_weight": "10",
            "water_weight": "20",
            "admixture_weight": "23.112",
        },
    )

    recipe = Recipe.objects.get(pk=got["id"])
    assert recipe.name == "hey"
    assert recipe.sand_weight == 0
    assert recipe.cement_weight == Decimal("0.2")
    assert recipe.gravel_weight == 10
    assert recipe.water_weight == 20
    assert recipe.admixture_weight == Decimal("23.112")


def test_ignored_values_are_set_to_their_defaults(api):
    got = api.post(
        f"{base_url}",
        data={
            "name": "hey",
            "water_weight": "20",
        },
    )

    recipe = Recipe.objects.get(pk=got["id"])
    assert recipe.sand_weight == 0
    assert recipe.cement_weight == 0
    assert recipe.gravel_weight == 0
    assert recipe.water_weight == 20
    assert recipe.admixture_weight == 0


def test_name_is_required(api):
    got = api.post(
        f"{base_url}",
        data={
            "water_weight": "20",
        },
        expected_status_code=400,
    )

    assert "name" in got


def test_ignore_id_in_request(api):
    got = api.post(
        f"{base_url}",
        data={
            "id": 100500,
            "name": "Yes!",
        },
    )

    recipe = Recipe.objects.get(pk=got["id"])
    assert recipe.id != 100500
    assert recipe.name == "Yes!"
