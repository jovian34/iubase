import pytest

from collections import namedtuple
from django.utils import timezone
from datetime import timedelta

from live_game_blog.models import Game, Team, Scoreboard, BlogEntry
from accounts.models import CustomUser
from accounts.tests.fixtures import (
    user_not_logged_in,
    user_iubase17,
    logged_user_schwarbs,
)


@pytest.fixture
def games(client, teams):
    iu_duke = Game.objects.create(
        home_team=teams.duke,
        away_team=teams.indiana,
        neutral_site=True,
        first_pitch=(timezone.now() + timedelta(days=1)),
    )
    iu_coastal = Game.objects.create(
        home_team=teams.coastal,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() + timedelta(days=2, hours=7)),
    )
    iu_gm = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.gm,
        neutral_site=True,
        first_pitch=(timezone.now() + timedelta(days=3)),
    )
    iu_mo_rain = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.miami_oh,
        neutral_site=False,
        first_pitch=(timezone.now() + timedelta(days=-315)),
    )
    iu_mo = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.miami_oh,
        neutral_site=False,
        first_pitch=(timezone.now() + timedelta(days=5)),
    )
    iu_uk_mon = Game.objects.create(
        home_team=teams.kentucky,
        home_seed=1,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() - timedelta(days=300)),
    )
    iu_uk_sun = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.kentucky,
        neutral_site=True,
        first_pitch=(timezone.now() - timedelta(days=301)),
    )
    iu_uk_sat = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.kentucky,
        neutral_site=True,
        first_pitch=(timezone.now() - timedelta(days=302)),
    )
    GameObj = namedtuple(
        "GameObj",
        "iu_duke iu_coastal iu_gm iu_mo iu_mo_rain iu_uk_mon iu_uk_sun iu_uk_sat",
    )
    return GameObj(
        iu_duke=iu_duke,
        iu_coastal=iu_coastal,
        iu_gm=iu_gm,
        iu_mo=iu_mo,
        iu_mo_rain=iu_mo_rain,
        iu_uk_mon=iu_uk_mon,
        iu_uk_sun=iu_uk_sun,
        iu_uk_sat=iu_uk_sat,
    )


@pytest.fixture
def scoreboard(client, games, user_not_logged_in):
    score_uk_mon = Scoreboard.objects.create(
        game=games.iu_uk_mon,
        scorekeeper=user_not_logged_in,
        game_status="final",
        inning_num=9,
        inning_part="Top",
        outs=3,
        home_runs=4,
        away_runs=2,
        home_hits=6,
        away_hits=10,
        home_errors=1,
        away_errors=1,
    )
    score_miami_rain = Scoreboard.objects.create(
        game=games.iu_mo_rain,
        scorekeeper=user_not_logged_in,
        game_status="cancelled",
        inning_num=3,
        inning_part="Bottom",
        outs=3,
        home_runs=7,
        away_runs=9,
        home_hits=12,
        away_hits=14,
        home_errors=1,
        away_errors=0,
    )
    score_uk_sun = Scoreboard.objects.create(
        game=games.iu_uk_sun,
        scorekeeper=user_not_logged_in,
        game_status="final",
        inning_num=9,
        inning_part="Bottom",
        outs=3,
        home_runs=6,
        away_runs=16,
        home_hits=12,
        away_hits=14,
        home_errors=1,
        away_errors=0,
    )
    score_uk_sat = Scoreboard.objects.create(
        game=games.iu_uk_sat,
        scorekeeper=user_not_logged_in,
        game_status="final",
        inning_num=9,
        inning_part="Top",
        outs=3,
        home_runs=5,
        away_runs=3,
        home_hits=8,
        away_hits=6,
        home_errors=1,
        away_errors=2,
    )
    score_duke = Scoreboard.objects.create(
        game=games.iu_duke, scorekeeper=user_not_logged_in, game_status="pre-game"
    )
    ScoreboardObj = namedtuple(
        "ScoreboardObj",
        "score_uk_mon, score_miami_rain, score_uk_sun, score_uk_sat score_duke",
    )
    return ScoreboardObj(
        score_uk_mon=score_uk_mon,
        score_miami_rain=score_miami_rain,
        score_uk_sun=score_uk_sun,
        score_uk_sat=score_uk_sat,
        score_duke=score_duke,
    )


@pytest.fixture
def blog_entries(client, games, user_not_logged_in, scoreboard):
    blog_uk_mon_y = BlogEntry.objects.create(
        game=games.iu_uk_mon,
        author=user_not_logged_in,
        blog_time=games.iu_uk_mon.first_pitch + timedelta(minutes=10),
        blog_entry="Bothwell walks the first batter",
        include_scoreboard=False,
    )
    blog_uk_mon_z = BlogEntry.objects.create(
        game=games.iu_uk_mon,
        author=user_not_logged_in,
        blog_time=games.iu_uk_mon.first_pitch + timedelta(minutes=165),
        blog_entry="Kentucky moves on to Super Regionals",
        include_scoreboard=True,
        scoreboard=scoreboard.score_uk_mon,
    )
    BlogEntryObj = namedtuple(
        "BlogEntryObj",
        "blog_uk_mon_y blog_uk_mon_z",
    )
    return BlogEntryObj(
        blog_uk_mon_y=blog_uk_mon_y,
        blog_uk_mon_z=blog_uk_mon_z,
    )
