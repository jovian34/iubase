import pytest
from django.urls import reverse
from datetime import date

from player_tracking.models import Player
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.views import set_player_properties

this_year = date.today().year


@pytest.mark.django_db
def test_draft_combine_attendees_set_to_current_last_year(
    client, players, transactions, annual_rosters, typical_mlb_draft_date
):
    response = client.get(reverse("players"), follow=True)
    nick = Player.objects.get(pk=players.nick_mitchell.pk)
    assert not nick.first_spring or nick.last_spring
    set_player_properties.set_player_props_get_errors()
    response = client.get(reverse("players"), follow=True)
    nick = Player.objects.get(pk=players.nick_mitchell.pk)
    assert nick.first_spring == this_year
    assert nick.last_spring == this_year


@pytest.mark.django_db
def test_draft_combine_attendees_renders(
    client, players, transactions, annual_rosters, typical_mlb_draft_date
):
    response = client.get(reverse("draft_combine_attendees", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert response.context["count"] == 2
    for item in ["Nick Mitchell", "College", "Hollister", "Freshman"]:
        assert item in response.content.decode()
