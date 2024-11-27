import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.models import Player, MLBDraftDate
from player_tracking.views import fall_players
from live_game_blog.tests.fixtures.teams import teams
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
    assert "not yet signed a National Letter of Intent" in str(response.content)


@pytest.mark.django_db
def test_incoming_players_excludes_signed_player (
    client, players, transactions, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("incoming_players", args=[f"{this_year + 1}"]))
    assert "Xavier" not in str(response.content)
    assert "not yet signed a National Letter of Intent" in str(response.content)


@pytest.mark.django_db
def test_nli_not_signed_not_logged_in_redirects_not_logged_in(
    client, players, transactions
):    
    response = client.get(
        reverse("incoming_players", args=[f"{this_year + 1}"]),
        follow=True,
    )
    assert response.status_code == 200
    assert "Password" in str(response.content)

