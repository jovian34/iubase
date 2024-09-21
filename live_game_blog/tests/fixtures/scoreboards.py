import pytest

from collections import namedtuple
from django.utils import timezone
from datetime import timedelta

from live_game_blog.tests.fixtures.games import games
from accounts.tests.fixtures import (
    user_not_logged_in,
    user_iubase17,
    logged_user_schwarbs,
)


from live_game_blog.models import Scoreboard


@pytest.fixture
def scoreboards(client, games, user_not_logged_in):
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
    score_coast_fut = Scoreboard.objects.create(
        game=games.iu_coastal,
        scorekeeper=user_not_logged_in,
        game_status="pre-game",
        inning_num=1,
        inning_part="Top",
        outs=0,
        home_runs=0,
        away_runs=0,
        home_hits=0,
        away_hits=0,
        home_errors=0,
        away_errors=0,
    )
    score_gm_fall = Scoreboard.objects.create(
        game=games.iu_gm_fall,
        scorekeeper=user_not_logged_in,
        game_status="pre-game",
        inning_num=1,
        inning_part="Top",
        outs=0,
        home_runs=0,
        away_runs=0,
        home_hits=0,
        away_hits=0,
        home_errors=0,
        away_errors=0,
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
        "score_uk_mon, score_coast_fut, score_gm_fall, score_miami_rain, score_uk_sun, score_uk_sat score_duke",
    )
    return ScoreboardObj(
        score_uk_mon=score_uk_mon,
        score_coast_fut=score_coast_fut,
        score_gm_fall=score_gm_fall,
        score_miami_rain=score_miami_rain,
        score_uk_sun=score_uk_sun,
        score_uk_sat=score_uk_sat,
        score_duke=score_duke,
    )