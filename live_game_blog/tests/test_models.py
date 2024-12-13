import pytest

from datetime import timedelta
from django.utils import timezone
from live_game_blog.tests.fixtures.games import (
    games,
    user_not_logged_in,
)
from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.blog import entries
from live_game_blog.tests.fixtures.scoreboards import scoreboards


@pytest.mark.django_db
def test_team_model_stored_all_fields(client, teams):
    assert teams.indiana.mascot == "Hoosiers"
    assert teams.duke.logo == "https://cdn.d1baseball.com/logos/teams/256/duke.png"
    assert teams.gm.team_name == "George Mason"
    assert not teams.indiana.stats
    assert not teams.indiana.roster


@pytest.mark.django_db
def test_team_model_string_def(client, teams):
    assert str(teams.indiana) == "Indiana"


@pytest.mark.django_db
def test_games_stored_neutral_site(client, games):
    assert games.iu_gm.neutral_site
    assert not games.iu_mo.neutral_site


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
def test_blog_model_sets_default_time(client, entries, user_not_logged_in):
    blog_time = entries.blog_uk_mon_z.blog_time
    expected_time = (timezone.now() - timedelta(days=300)) + timedelta(minutes=165)
    assert expected_time - blog_time < timedelta(seconds=5)
