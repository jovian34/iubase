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
        roster="https://uclabruins.com/sports/baseball/roster",
    )
    unc = lgb_models.Team.objects.create(
        team_name="North Carolina",
        mascot="Tarheels",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/north-carolina.svg",
        roster="https://goheels.com/sports/baseball/roster",
    )
    rut = lgb_models.Team.objects.create(
        team_name="Rutgers",
        mascot="Scarlett Knights",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/rutgers.svg",
        roster="https://scarletknights.com/sports/baseball/roster",
    )
    chicago = lgb_models.Team.objects.create(
        team_name="Chicago",
        mascot="Maroons",
        logo="https://www.pngkit.com/png/full/267-2678346_chicago-maroons-logo-university-of-chicago-c.png",
        roster="https://athletics.uchicago.edu/sports/baseball/roster",
    )
    nw = lgb_models.Team.objects.create(
        team_name="Northwestern",
        mascot="Wildcats",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/northwestern.svg",
        roster="https://nusports.com/sports/baseball/roster",
    )
    neb = lgb_models.Team.objects.create(
        team_name="Nebraska",
        mascot="Cornhuskers",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/nebraska.svg",
        roster="https://huskers.com/sports/baseball/roster",
    )
    ore = lgb_models.Team.objects.create(
        team_name="Oregon",
        mascot="Ducks",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/oregon.svg",
        roster="https://goducks.com/sports/baseball/roster/",
    )
    mich = lgb_models.Team.objects.create(
        team_name="Michigan",
        mascot="Wolverines",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/michigan.svg",
        roster="https://mgoblue.com/sports/baseball/roster",
    )
    usc = lgb_models.Team.objects.create(
        team_name="USC",
        mascot="Trojans",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/southern-california.svg",
        roster="https://usctrojans.com/sports/baseball/roster",
    )
    wash = lgb_models.Team.objects.create(
        team_name="Washington",
        mascot="Huskies",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/washington.svg",
        roster="https://gohuskies.com/sports/baseball/roster",
    )
    psu = lgb_models.Team.objects.create(
        team_name="Penn State",
        mascot="Nittany Lions",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/penn-st.svg",
        roster="https://gopsusports.com/sports/baseball/roster",
    )
    ill = lgb_models.Team.objects.create(
        team_name="Illinois",
        mascot="Fighting Illini",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/illinois.svg",
        roster="https://fightingillini.com/sports/baseball/roster",
    )
    sparty = lgb_models.Team.objects.create(
        team_name="Michigan State",
        mascot="Spartans",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/michigan-st.svg",
        roster="https://msuspartans.com/sports/baseball/roster",
    )
    terps = lgb_models.Team.objects.create(
        team_name="Maryland",
        mascot="Terrapins",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/maryland.svg",
        roster="https://umterps.com/sports/baseball/roster",
    )
    boilers = lgb_models.Team.objects.create(
        team_name="Purdue",
        mascot="Boilermakers",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/purdue.svg",
        roster="https://purduesports.com/sports/baseball/roster",
    )
    minny = lgb_models.Team.objects.create(
        team_name="Minnesota",
        mascot="Golden Gophers",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/minnesota.svg",
        roster="https://gophersports.com/sports/baseball/roster"
    )
    osu = lgb_models.Team.objects.create(
        team_name="Ohio State",
        mascot="Buckeyes",
        logo="https://www.ncaa.com/sites/default/files/images/logos/schools/bgl/ohio-st.svg",
        roster="https://ohiostatebuckeyes.com/sports/baseball/roster",
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
        "unc",
        "rut",
        "chicago",
        "nw",
        "neb",
        "ore",
        "mich",
        "usc",
        "wash",
        "psu",
        "ill",
        "sparty",
        "terps",
        "boilers",
        "minny",
        "osu",
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
        unc=unc,
        rut=rut,
        chicago=chicago,
        nw=nw,
        neb=neb,
        ore=ore,
        mich=mich,
        usc=usc,
        wash=wash,
        psu=psu,
        ill=ill,
        sparty=sparty,
        terps=terps,
        boilers=boilers,
        minny=minny,
        osu=osu,
    )
