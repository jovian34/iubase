import pytest

from collections import namedtuple

from live_game_blog import models as lgb_models


@pytest.fixture
def teams(client):
    indiana = lgb_models.Team.objects.create(
        team_name="Indiana",
        mascot="Hoosiers",
        logo="https://cdn.d1baseball.com/logos/teams/256/indiana.png",
        roster="https://iuhoosiers.com/sports/baseball/roster",
    )
    duke = lgb_models.Team.objects.create(
        team_name="Duke",
        mascot="Blue Devils",
        logo="https://cdn.d1baseball.com/logos/teams/256/duke.png",
        roster="https://goduke.com/sports/baseball/roster/",
    )
    coastal = lgb_models.Team.objects.create(
        team_name="Coastal Carolina",
        mascot="Chanticleers",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143355/coastcar.png",
        roster="https://goccusports.com/sports/baseball/roster",
    )
    kentucky = lgb_models.Team.objects.create(
        team_name="Kentucky",
        mascot="Wildcats",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143618/kentucky.png",
        roster="https://ukathletics.com/sports/baseball/roster/",
    )
    gm = lgb_models.Team.objects.create(
        team_name="George Mason",
        mascot="Patriots",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143506/georgemas.png",
        roster="https://gomason.com/sports/baseball/roster",
    )
    miami_oh = lgb_models.Team.objects.create(
        team_name="Miami (Ohio)",
        mascot="RedHawks",
        logo="https://cdn.d1baseball.com/uploads/2023/12/21143717/miamioh.png",
        roster="https://miamiredhawks.com/sports/baseball/roster",
    )
    iowa = lgb_models.Team.objects.create(
        team_name="Iowa",
        mascot="Hawkeyes",
        logo="https://web2.ncaa.org/ncaa_style/img/All_Logos/sm/312.gif",
        roster="https://hawkeyesports.com/sports/baseball/roster/season/",
    )
    ucla = lgb_models.Team.objects.create(
        team_name="UCLA",
        mascot="Bruins",
        logo="https://web2.ncaa.org/ncaa_style/img/All_Logos/sm/110.gif",
        roster="https://uclabruins.com/sports/baseball/roster"
    )
    team_list = [
        "indiana",
        "duke", 
        "coastal",
        "kentucky",
        "gm",
        "miami_oh",
        "iowa",
        "ucla",
    ]
    TeamObj = namedtuple("TeamObj", team_list)
    return TeamObj(
        indiana=indiana,
        duke=duke,
        coastal=coastal,
        kentucky=kentucky,
        gm=gm,
        miami_oh=miami_oh,
        iowa=iowa,
        ucla=ucla,
    )
