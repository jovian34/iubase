import pytest
from django.urls import reverse

from player_tracking.tests.fixtures.players import players


@pytest.mark.django_db
def test_add_accolade_partial_renders_form(client, players):
    response = client.get(
        reverse("add_accolade", args=[str(players.devin_taylor.pk)]),
    )
    assert response.status_code == 200
    assert "Name of accolade" in str(response.content)
    assert "Date issued" in str(response.content)
    assert "Sponsor Organization" in str(response.content)
    assert "Detailed description" in str(response.content)
    assert "Web link for announcement" in str(response.content)
    assert "Applicable college roster" in str(response.content)


@pytest.mark.django_db
def test_add_accolade_partial_renders_form_with_only_one_players_rosters(client, players):
    response = client.get(
        reverse("add_accolade", args=[str(players.devin_taylor.pk)]),
    )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)