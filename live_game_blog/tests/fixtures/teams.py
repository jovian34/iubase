import pytest

from collections import namedtuple

from live_game_blog.models import Team


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
        logo="https://cdn.d1baseball.com/logos/teams/256/duke.png",
    )
    coastal = Team.objects.create(
        team_name="Coastal Carolina",
        mascot="Chanticleers",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143355/coastcar.png",
    )
    kentucky = Team.objects.create(
        team_name="Kentucky",
        mascot="Wildcats",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143618/kentucky.png",
    )
    gm = Team.objects.create(
        team_name="George Mason",
        mascot="Patriots",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143506/georgemas.png",
    )
    miami_oh = Team.objects.create(
        team_name="Miami (Ohio)",
        mascot="RedHawks",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143717/miamioh.png",
    )
    TeamObj = namedtuple("TeamObj", "indiana duke coastal kentucky gm miami_oh")
    return TeamObj(
        indiana=indiana,
        duke=duke,
        coastal=coastal,
        kentucky=kentucky,
        gm=gm,
        miami_oh=miami_oh,
    )