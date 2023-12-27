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
    game_last_week = Game.objects.create(
        home_team=teams.kentucky,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() - timedelta(days=10)),
    )
    GameObj = namedtuple("GameObj", "game_tomorrow game_in_two_days game_last_week")
    return GameObj(
        game_tomorrow=game_tommorrow, 
        game_in_two_days=game_in_two_days, 
        game_last_week=game_last_week
    )
