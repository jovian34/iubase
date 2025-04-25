import pytest

from collections import namedtuple

from live_game_blog.models import Team


@pytest.fixture
def teams(client):
    indiana = Team.objects.create(
        team_name="Indiana",
        mascot="Hoosiers",
        logo="https://cdn.d1baseball.com/logos/teams/256/indiana.png",
        roster="https://iuhoosiers.com/sports/baseball/roster",
    )
    duke = Team.objects.create(
        team_name="Duke",
        mascot="Blue Devils",
        logo="https://cdn.d1baseball.com/logos/teams/256/duke.png",
        roster="https://goduke.com/sports/baseball/roster/",
    )
    coastal = Team.objects.create(
        team_name="Coastal Carolina",
        mascot="Chanticleers",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143355/coastcar.png",
        roster="https://goccusports.com/sports/baseball/roster",
    )
    kentucky = Team.objects.create(
        team_name="Kentucky",
        mascot="Wildcats",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143618/kentucky.png",
        roster="https://ukathletics.com/sports/baseball/roster/",
    )
    gm = Team.objects.create(
        team_name="George Mason",
        mascot="Patriots",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143506/georgemas.png",
        roster="https://gomason.com/sports/baseball/roster",
    )
    miami_oh = Team.objects.create(
        team_name="Miami (Ohio)",
        mascot="RedHawks",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143717/miamioh.png",
        roster="https://miamiredhawks.com/sports/baseball/roster",
    )
    iowa = Team.objects.create(
        team_name="Iowa",
        mascot="Hawkeyes",
        logo="https://web2.ncaa.org/ncaa_style/img/All_Logos/sm/312.gif",
        roster="https://hawkeyesports.com/sports/baseball/roster/season/",
    )
    TeamObj = namedtuple("TeamObj", "indiana duke coastal kentucky gm miami_oh iowa")
    return TeamObj(
        indiana=indiana,
        duke=duke,
        coastal=coastal,
        kentucky=kentucky,
        gm=gm,
        miami_oh=miami_oh,
        iowa=iowa,
    )