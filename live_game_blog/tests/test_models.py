import pytest

from datetime import timedelta, date
from django.utils import timezone
from live_game_blog.tests.fixtures.games import (
    games,
    user_not_logged_in,
)
from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.home_stadium import home_stadium
from live_game_blog.tests.fixtures.blog import entries
from live_game_blog.tests.fixtures.scoreboards import scoreboards


@pytest.mark.django_db
def test_team_model_stored_all_fields(client, teams):
    assert teams.indiana.mascot == "Hoosiers"
    assert teams.duke.logo == "https://cdn.d1baseball.com/logos/teams/256/duke.png"
    assert teams.gm.team_name == "George Mason"
    assert teams.miami_oh.mascot == "RedHawks"
    assert not teams.indiana.stats
    assert teams.miami_oh.roster == "https://miamiredhawks.com/sports/baseball/roster"


@pytest.mark.django_db
def test_team_model_string_def(client, teams):
    assert str(teams.indiana) == "Indiana"


@pytest.mark.django_db
def test_stadium_model_stored_all_fields(client, stadiums):
    assert stadiums.bart.address == "1873 N Fee Ln"
    assert stadiums.bart.city == "Bloomington"
    assert stadiums.bart.country == "USA"
    assert stadiums.bart.timezone == "America/New_York"
    assert stadiums.bart.lat == 39.18452321031082
    assert stadiums.bart.long == -86.52270607828599


@pytest.mark.django_db
def test_stadium_model_string_def(client, stadiums):
    assert str(stadiums.bart) == "1873 N Fee Ln | Bloomington, IN USA"


@pytest.mark.django_db
def test_stadium_config_model_stored_all_fields(client, stadiums, stadium_configs):
    assert stadium_configs.bart_2013.stadium == stadiums.bart
    assert stadium_configs.bart_2013.config_date == date(2013,3,1)
    assert stadium_configs.bart_2013.surface_inf == "artificial"
    assert stadium_configs.bart_2013.surface_out == "artificial"
    assert stadium_configs.bart_2013.surface_mound == "artificial"
    assert stadium_configs.bart_2013.photo == "https://live.staticflickr.com/65535/54870456854_577c2962c0_c.jpg"
    assert stadium_configs.bart_2013.left == 330
    assert stadium_configs.bart_2013.right == 330
    assert stadium_configs.bart_2013.center == 400
    assert stadium_configs.surprise_2002.lights
    assert stadium_configs.surprise_2002.capacity == 10714
    assert stadium_configs.bart_2013.home_dugout == "third"
    assert stadium_configs.bart_2013.orientation == 45


@pytest.mark.django_db
def test_stadium_config_model_string_def(client, stadiums, stadium_configs):
    assert str(stadium_configs.bart_2013) == "Bart Kaufman Field - 2013"


@pytest.mark.django_db
def test_home_stadium_model_stored_all_fields(client, stadiums, home_stadium, teams, stadium_configs):
    assert home_stadium.bart_2013.team == teams.indiana
    assert home_stadium.bart_2013.stadium_config == stadium_configs.bart_2013
    assert home_stadium.bart_2013.designate_date == date(2013,3,1)


@pytest.mark.django_db
def test_home_stadium_model_string_def(client, stadiums, home_stadium):
    assert str(home_stadium.bart_2013) == "Indiana: Bart Kaufman Field - 2013"


@pytest.mark.django_db
def test_games_stored_neutral_site(client, games):
    assert games.iu_gm.neutral_site
    assert not games.iu_mo.neutral_site


@pytest.mark.django_db
def test_games_stored_stadium_for_neutral_game(client, games, stadiums):
    assert games.iu_duke.stadium == stadiums.surprise


@pytest.mark.django_db
def test_game_model_string_def(client, games):
    assert "Indiana at Kentucky" in str(games.iu_uk_mon)


@pytest.mark.django_db
def test_game_model_string_def_neutral(client, games):
    assert "George Mason vs. Indiana" in str(games.iu_gm)


@pytest.mark.django_db
def test_scoreboard_sets_default_time(client, scoreboards, user_not_logged_in):
    score_time = scoreboards.score_uk_mon.update_time
    assert timezone.now() - score_time < timedelta(seconds=2)


@pytest.mark.django_db
def test_scoreboard_model_string_def(client, scoreboards, user_not_logged_in):
    assert str(scoreboards.score_uk_sat) == "Kentucky-3, Indiana-5 | Top Inning: 9"


@pytest.mark.django_db
def test_blog_model_string_def(client, entries, user_not_logged_in):
    assert "denato: " in str(entries.blog_uk_mon_z)


@pytest.mark.django_db
def test_blog_model_not_html(client, entries, user_not_logged_in):
    assert not entries.blog_uk_mon_z.is_raw_html


@pytest.mark.django_db
def test_blog_model_is_a_photo_only(client, entries, user_not_logged_in):
    assert entries.blog_uk_mon_photo.is_photo_only


@pytest.mark.django_db
def test_blog_model_sets_default_time(client, entries, user_not_logged_in):
    blog_time = entries.blog_uk_mon_z.blog_time
    expected_time = (timezone.now() - timedelta(days=300)) + timedelta(minutes=165)
    assert expected_time - blog_time < timedelta(seconds=5)
