import pytest
from django.urls import reverse
from datetime import date

from live_game_blog.tests.fixtures import teams
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.prof_org import prof_orgs


@pytest.mark.django_db
def test_portal_page_renders(client, players, teams, annual_rosters, transactions):
    response = client.get(reverse("portal", args=[str(date.today().year)]))
    assert response.status_code == 200
    assert "Total Players in the Portal: 1"
    assert "Brooks Ey" in str(response.content)
    assert "Devin" not in str(response.content)