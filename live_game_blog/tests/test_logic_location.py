import pytest

from live_game_blog.logic import location
from live_game_blog.tests.fixtures.games import games
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.teams import teams


@pytest.mark.django_db
def test_location_rejects_game_without_home_stadium(
    games,
    stadiums,
    stadium_configs,
    teams,
):
    game = games.iu_duke
    game.neutral_site = False

    with pytest.raises(
        ValueError,
        match="No home stadium set for Duke for the date of first pitch",
    ):
        location.get_lat_and_long_of_stadium(game)
