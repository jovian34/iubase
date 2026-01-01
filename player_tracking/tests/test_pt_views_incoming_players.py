import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.views import set_player_properties
from player_tracking.views.fall import fall_landing
from live_game_blog.tests.fixtures.teams import teams


this_year = date.today().year


@pytest.mark.django_db
def test_incoming_players_renders(client, players, transactions):
    set_player_properties.set_player_props_get_errors()
    response = client.get(reverse("incoming_players", args=[f"{this_year + 1}"]))
    assert "Owen" in response.content.decode()
    assert f"Incoming players for Fall {this_year + 1}" in response.content.decode()


@pytest.mark.django_db
def test_incoming_players_places_hs_under_correct_nli_headers_player(
    client, players, transactions
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(reverse("incoming_players", args=[f"{this_year + 1}"]))
    output = response.content.decode()
    xavier = output.find("Xavier")
    owen = output.find("Owen")
    nli_head = output.find("from high school pending")
    assert nli_head > xavier
    assert nli_head < owen


@pytest.mark.django_db
def test_incoming_players_places_transfers_under_correct_header(
    client, players, transactions
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(reverse("incoming_players", args=[f"{this_year}"]))
    output = response.content.decode()
    gilley = output.find("Gilley")
    transfer_head = output.find("Transfer Commits")
    assert gilley > transfer_head
