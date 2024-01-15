import pytest
from django.urls import reverse

from player_tracking.tests.fixtures import players


@pytest.mark.django_db
def test_index(client, players):
    response = client.get(reverse("players"))
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)
