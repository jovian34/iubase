import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)
from player_tracking.tests.fixtures.players import players


this_year = date.today().year

@pytest.mark.django_db
def test_summer_assignments_page_renders(
    client, players, summer_assign, summer_leagues, summer_teams
):
    response = client.get(reverse("summer_assignments", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)
    assert "Ryan Kraft" in str(response.content)