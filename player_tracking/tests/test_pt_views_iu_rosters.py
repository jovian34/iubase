import pytest
from django.urls import reverse
from datetime import date

from live_game_blog.tests.fixtures.teams import teams
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.transactions import transactions

this_year = date.today().year


@pytest.mark.django_db
def test_fall_roster_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("fall_roster", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert "Total Roster Length: 4" in str(response.content)
    assert f"Fall {this_year - 1} Roster" in str(response.content)
    assert "Nathan Ball" in str(response.content)
    assert "Nick Mitchell" in str(response.content)
    assert "Jack Moffitt" in str(response.content)
    assert "Brayden" not in str(response.content)


@pytest.mark.django_db
def test_spring_roster_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("spring_roster", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert "Total Roster Length: 2" in str(response.content)
    assert f"Spring {this_year - 1} Roster" in str(response.content)
    assert "Nick Mitchell" not in str(response.content)
    assert "Devin Taylor" in str(response.content)