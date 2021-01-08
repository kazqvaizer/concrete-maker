from decimal import Decimal

import pytest

from production.models import Batch

pytestmark = [
    pytest.mark.django_db,
]

base_url = "/api/v1/production/batches/"


def test_add_response(api, recipe):
    got = api.post(
        f"{base_url}",
        data={
            "recipe": recipe.id,
            "volume": "2.0",
            "sand_weight": "0",
            "cement_weight": "0.2",
            "gravel_weight": "10",
            "water_weight": "20",
            "admixture_weight": "23.112",
        },
    )

    assert "id" in got
    assert got["recipe"] == recipe.id
    assert got["volume"] == "2.000"
    assert got["sand_weight"] == "0.000"
    assert got["cement_weight"] == "0.200"
    assert got["gravel_weight"] == "10.000"
    assert got["water_weight"] == "20.000"
    assert got["admixture_weight"] == "23.112"


def test_actually_stored(api, recipe):
    got = api.post(
        f"{base_url}",
        data={
            "recipe": recipe.id,
            "volume": "2.0",
            "sand_weight": "0",
            "cement_weight": "0.2",
            "gravel_weight": "10",
            "water_weight": "20",
            "admixture_weight": "23.112",
        },
    )

    batch = Batch.objects.get(pk=got["id"])
    assert batch.recipe == recipe
    assert batch.volume == 2
    assert batch.sand_weight == 0
    assert batch.cement_weight == Decimal("0.2")
    assert batch.gravel_weight == 10
    assert batch.water_weight == 20
    assert batch.admixture_weight == Decimal("23.112")


def test_ignored_values_are_set_to_their_defaults(api, recipe):
    got = api.post(
        f"{base_url}",
        data={
            "recipe": recipe.id,
            "water_weight": "20",
        },
    )

    batch = Batch.objects.get(pk=got["id"])
    assert batch.recipe == recipe
    assert batch.volume == 0
    assert batch.sand_weight == 0
    assert batch.cement_weight == 0
    assert batch.gravel_weight == 0
    assert batch.water_weight == 20
    assert batch.admixture_weight == 0


def test_recipe_is_required(api):
    got = api.post(
        f"{base_url}",
        data={
            "water_weight": "20",
        },
        expected_status_code=400,
    )

    assert "recipe" in got


def test_existing_recipe_is_required(api):
    got = api.post(
        f"{base_url}",
        data={
            "recipe": 100500,
            "water_weight": "20",
        },
        expected_status_code=400,
    )

    assert "recipe" in got


def test_ignore_id_in_request(api, recipe):
    got = api.post(
        f"{base_url}",
        data={
            "id": 100500,
            "recipe": recipe.id,
        },
    )

    batch = Batch.objects.get(pk=got["id"])
    assert batch.id != 100500
    assert batch.recipe == recipe
