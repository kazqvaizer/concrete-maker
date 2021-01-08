import pytest

from production.models import Batch

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def batch(mixer, recipe):
    return mixer.blend("production.Batch", recipe=recipe, volume=2.2, sand_weight=10.5)


base_url = "/api/v1/production/batches/"


def test_delete(api, batch):
    api.delete(f"{base_url}{batch.id}/")

    with pytest.raises(Batch.DoesNotExist):
        batch.r()
