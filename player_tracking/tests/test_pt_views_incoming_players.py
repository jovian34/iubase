import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.views import fall_players
from accounts.tests.fixtures import logged_user_schwarbs

this_year = date.today().year


@pytest.mark.django_db
def test_incoming_players_renders(
    client, players, transactions, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("incoming_players", args=[f"{this_year + 1}"]))
    assert "Owen" in str(response.content)
    assert f"Incoming players for Fall {this_year + 1}" in str(response.content)


@pytest.mark.django_db
def test_incoming_players_places_hs_under_correct_nli_headers_player (
    client, players, transactions, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("incoming_players", args=[f"{this_year + 1}"]))
    output = str(response.content)
    xavier = output.find("Xavier")
    owen = output.find("Owen")
    nli_head = output.find("with confirmed National")
    assert nli_head < xavier
    assert nli_head > owen


@pytest.mark.django_db
def test_incoming_players_places_transfers_under_correct_header (
    client, players, transactions, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("incoming_players", args=[f"{this_year}"]))
    output = str(response.content)
    gilley = output.find("Gilley")
    transfer_head = output.find("Transfer Commits")
    assert gilley > transfer_head

