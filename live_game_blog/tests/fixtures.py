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
    TeamObj = namedtuple(
        "TeamObj", 
        "indiana duke coastal kentucky gm miami_oh"
    )
    return TeamObj(
        indiana=indiana, 
        duke=duke, 
        coastal=coastal, 
        kentucky=kentucky, 
        gm=gm,
        miami_oh=miami_oh
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
    iu_mo = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.miami_oh,
        neutral_site=False,
        first_pitch=(timezone.now() + timedelta(days=5))
    )
    iu_uk_mon = Game.objects.create(
        home_team=teams.kentucky,
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
        "iu_duke iu_coastal iu_gm iu_mo iu_uk_mon iu_uk_sun iu_uk_sat"
    )
    return GameObj(
        iu_duke=iu_duke, 
        iu_coastal=iu_coastal,
        iu_gm=iu_gm,
        iu_mo=iu_mo, 
        iu_uk_mon=iu_uk_mon,
        iu_uk_sun=iu_uk_sun,
        iu_uk_sat=iu_uk_sat,
    )

@pytest.fixture
def scoreboard(client, games, user_1):
    score_uk_mon = Scoreboard.objects.create(
        game=games.iu_uk_mon,
        scorekeeper=user_1,
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
    score_uk_sun = Scoreboard.objects.create(
        game=games.iu_uk_sun,
        scorekeeper=user_1,
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
        scorekeeper=user_1,
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
    ScoreboardObj = namedtuple(
        "ScoreboardObj", 
        "score_uk_mon, score_uk_sun, score_uk_sat"
    )
    return ScoreboardObj(
        score_uk_mon=score_uk_mon,
        score_uk_sun=score_uk_sun,
        score_uk_sat=score_uk_sat,
    )

@pytest.fixture
def blog_entries(client, games, user_1, scoreboard):
    blog_uk_mon_z = BlogEntry.objects.create(
        game=games.iu_uk_mon,
        author=user_1,
        blog_time=games.iu_uk_mon.first_pitch + timedelta(minutes=165),
        blog_entry="Kentucky moves on to Super Regionals",
        include_scoreboard=True,
        scoreboard=scoreboard.score_uk_mon,
    )
    BlogEntryObj = namedtuple(
        "BlogEntryObj",
        "blog_uk_mon_z",
    )
    return BlogEntryObj(
        blog_uk_mon_z=blog_uk_mon_z,
    )