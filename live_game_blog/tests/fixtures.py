import pytest

from collections import namedtuple
from django.utils import timezone
from datetime import timedelta

from ..models import Game, Team


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
    game_tommorrow = Game.objects.create(
        home_team=teams.duke,
        away_team=teams.indiana,
        neutral_site=True,
        first_pitch=(timezone.now() + timedelta(days=1)),
    )
    game_in_two_days = Game.objects.create(
        home_team=teams.coastal,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() + timedelta(days=2)),
    )
    game_last_year = Game.objects.create(
        home_team=teams.kentucky,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() - timedelta(days=300)),
        inning_num=9,
        inning_part="final",
        outs=3,
        home_runs=4,
        away_runs=2,
        home_hits=6,
        away_hits=10,
        home_errors=1,
        away_errors=1
    )
    GameObj = namedtuple("GameObj", "game_tomorrow game_in_two_days game_last_year")
    return GameObj(
        game_tomorrow=game_tommorrow, 
        game_in_two_days=game_in_two_days, 
        game_last_year=game_last_year
    )
