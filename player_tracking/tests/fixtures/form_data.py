import pytest

from collections import namedtuple
from datetime import date

from player_tracking.tests.fixtures.summer import (
    summer_leagues,
    summer_teams,
)
from player_tracking.tests.fixtures.prof_org import prof_orgs
from live_game_blog.tests.fixtures.teams import teams


this_year = date.today().year


@pytest.fixture
def forms(summer_leagues, summer_teams, teams, prof_orgs):
    phillip_glasser_new = {
        "first": ["Phillip"],
        "last": ["Glasser"],
        "hsgrad_year": [f"{this_year - 6}"],
        "high_school": ["Tallmadge"],
        "home_city": ["Tallmadge"],
        "home_state": ["OH"],
        "home_country": ["USA"],
        "headshot": [
            "https://www.prepbaseballreport.com/passets/photo/OH/8542307196-PhillipGlasser.png"
        ],
        "birthdate": [f"{this_year - 25}-12-03"],
        "bats": ["Left"],
        "throws": ["Right"],
        "height": [72],
        "weight": [170],
        "trans_event": ["Verbal Commitment from College"],
        "trans_date": [f"{this_year - 3}-06-15"],
        "primary_position": ["Shortstop"],
        "citation": [
            "https://d1baseball.com/transfers/2021-22-d1baseball-transfer-tracker/"
        ],
    }
    summer_assignment_new = {
        "summer_year": [f"{this_year}"],
        "summer_team": [str(summer_teams.gb.pk)],
        "summer_league": [str(summer_leagues.nw.pk)],
    }
    nick_mitchell_two_years_past = {
        "spring_year": [f"{this_year - 2}"],
        "team": [str(teams.duke.pk)],
        "jersey": ["29"],
        "status": ["Spring Roster"],
        "primary_position": ["Centerfield"],
        "secondary_position": [],
    }
    risedorph_drafted = {
        "trans_event": ["Drafted"],
        "trans_date": [str(date(this_year, 7, 17))],
        "citation": ["https://www.mlb.com/draft/tracker"],
        "other_team": [],
        "prof_org": [prof_orgs.d_backs.pk],
        "bonus_or_slot": ["150000"],
        "comment": ["Expected to go over slot value."],
    }
    devin_taylor_edited = {
        "first": ["Devin"],
        "last": ["Taylor"],
        "hsgrad_year": [f"{this_year - 2}"],
        "high_school": ["LaSalle"],
        "home_city": ["Cincinnati"],
        "home_state": ["OH"],
        "home_country": ["USA"],
        "headshot": ["https://iubase.com/wp-content/uploads/2023/03/Taylor-still_00001-2.jpg"],
        "action_shot": ["https://live.staticflickr.com/65535/54132418776_e7cc1bcd11_k.jpg"],
        "birthdate": [],
        "bats": ["Left"],
        "throws": ["Left"],
        "height": [],
        "weight": [],
        "primary_position": [],
    }
    FormObj = namedtuple(
        "FormObj",
        "phillip_glasser_new summer_assignment_new nick_mitchell_two_years_past risedorph_drafted devin_taylor_edited",
    )
    return FormObj(
        phillip_glasser_new=phillip_glasser_new,
        summer_assignment_new=summer_assignment_new,
        nick_mitchell_two_years_past=nick_mitchell_two_years_past,
        risedorph_drafted=risedorph_drafted,
        devin_taylor_edited=devin_taylor_edited,
    )



