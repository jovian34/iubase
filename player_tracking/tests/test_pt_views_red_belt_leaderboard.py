from datetime import date

import pytest
from django.urls import reverse

from accounts.tests.fixtures import logged_user_schwarbs
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.models import Accolade, AnnualRoster
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players


this_year = date.today().year


@pytest.mark.django_db
def test_red_belt_leaderboard_page_renders(admin_client):
    response = admin_client.get(reverse("red_belt_leaderboard", args=[this_year]))
    assert response.status_code == 200

