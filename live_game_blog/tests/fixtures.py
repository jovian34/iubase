import pytest

from collections import namedtuple
from django.utils import timezone
from datetime import timedelta

from live_game_blog.models import Game, Team, Scoreboard, BlogEntry
from accounts.models import CustomUser

@pytest.fixture
def user_1(client):
    user = CustomUser.objects.create_user("user_one")
    user.set_password("This is my new passphrase")
    return user


@pytest.fixture
def teams(client):
    indiana = Team.objects.create(
        team_name="Indiana",
        mascot="Hoosiers",
        logo="https://cdn.d1baseball.com/logos/teams/256/indiana.png",
    )
    duke = Team.objects.create(
        team_name="Duke",
        mascot="Blue Devils",
        logo="https://cdn.d1baseball.com/logos/teams/256/duke.png"
    )
    coastal = Team.objects.create(
        team_name="Coastal Carolina",
        mascot="Chanticleers",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143355/coastcar.png",
    )
    kentucky = Team.objects.create(
        team_name="Kentucky",
        mascot="Wildcats",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143618/kentucky.png"
    )
    TeamObj = namedtuple("TeamObj", "indiana duke coastal kentucky")
    return TeamObj(indiana=indiana, duke=duke, coastal=coastal, kentucky=kentucky)

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
        first_pitch=(timezone.now() + timedelta(days=2)),
    )
    iu_uk_mon = Game.objects.create(
        home_team=teams.kentucky,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() - timedelta(days=300)),
    )
    GameObj = namedtuple("GameObj", "iu_duke iu_coastal iu_uk_mon")
    return GameObj(
        iu_duke=iu_duke, 
        iu_coastal=iu_coastal, 
        iu_uk_mon=iu_uk_mon,
    )

@pytest.fixture
def scoreboard(client, games, user_1):
    status_iu_uk_mon = Scoreboard.objects.create(
        game=games.iu_uk_mon,
        scorekeeper=user_1,
        game_status="final",
        inning_num=9,
        inning_part="top",
        outs=3,
        home_runs=4,
        away_runs=2,
        home_hits=6,
        away_hits=10,
        home_errors=1,
        away_errors=1,
    )
    ScoreboardObj = namedtuple("ScoreboardObj", "status_iu_uk_mon")
    return ScoreboardObj(status_iu_uk_mon=status_iu_uk_mon)