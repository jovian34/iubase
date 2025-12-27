import pytest
import datetime

from django import urls

from live_game_blog.tests.fixtures.games_annual import games_annual
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.teams import teams


@pytest.mark.django_db
def test_schedule_renders_selected_season_games_only(client, games_annual, stadiums, stadium_configs, teams):
    if datetime.date.today().month > 8:
        spring_year = datetime.date.today().year + 1
    else:
        spring_year = datetime.date.today().year
    response = client.get(urls.reverse("schedule", args=[spring_year]))
    assert response.status_code == 200
    assert "Miami (Ohio) <em>@</em>  Indiana" in response.content.decode()
    assert "Indiana <em>@</em>  Iowa" in response.content.decode()
    assert "Indiana <em>vs.</em>  Duke" in response.content.decode()
    assert "Kentucky" not in response.content.decode()
    assert "Coastal" not in response.content.decode()
    