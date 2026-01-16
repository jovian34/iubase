import pytest

from collections import namedtuple
from django.utils import timezone
from datetime import timedelta

from live_game_blog.tests.fixtures.games import games
from live_game_blog.tests.fixtures.stadiums import stadiums
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
    score_coast_ip = Scoreboard.objects.create(
        game=games.iu_coastal_ip,
        scorekeeper=user_not_logged_in,
        game_status="in-progress",
        inning_num=3,
        inning_part="Top",
        outs=1,
        home_runs=6,
        away_runs=0,
        home_hits=5,
        away_hits=0,
        home_errors=0,
        away_errors=1,
    )
    score_iu_uk_far = Scoreboard.objects.create(
        game=games.iu_uk_far_future,
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
    score_iowa_fut = Scoreboard.objects.create(
        game=games.iu_iowa,
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
    score_iu_duke_ly = Scoreboard.objects.create(
        game=games.iu_duke_ly,
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
    score_iu_duke_23_fall = Scoreboard.objects.create(
        game=games.iu_duke_23_fall,
        scorekeeper=user_not_logged_in,
        game_status="final",
        inning_num=14,
        inning_part="Bottom",
        outs=3,
        home_runs=18,
        away_runs=16,
        home_hits=20,
        away_hits=14,
        home_errors=1,
        away_errors=2,
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
    scoreboard_list = [
        "score_uk_mon",
        "score_coast_fut",
        "score_coast_ip",
        "score_gm_fall",
        "score_iu_uk_far",
        "score_iowa_fut",
        "score_miami_rain",
        "score_uk_sun",
        "score_iu_duke_ly",
        "score_iu_duke_23_fall",
        "score_uk_sat",
        "score_duke",
    ]
    ScoreboardObj = namedtuple("ScoreboardObj", scoreboard_list)
    return ScoreboardObj(
        score_uk_mon=score_uk_mon,
        score_coast_fut=score_coast_fut,
        score_coast_ip=score_coast_ip,
        score_gm_fall=score_gm_fall,
        score_iowa_fut=score_iowa_fut,
        score_miami_rain=score_miami_rain,
        score_uk_sun=score_uk_sun,
        score_iu_duke_ly=score_iu_duke_ly,
        score_iu_duke_23_fall=score_iu_duke_23_fall,
        score_uk_sat=score_uk_sat,
        score_duke=score_duke,
        score_iu_uk_far=score_iu_uk_far,
    )
