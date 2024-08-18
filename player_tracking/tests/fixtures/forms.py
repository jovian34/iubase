import pytest

from collections import namedtuple
from datetime import date

from player_tracking.tests.fixtures.summer import (
    summer_leagues,
    summer_teams,
)


this_year = date.today().year


@pytest.fixture
def forms(summer_leagues, summer_teams):
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
    FormObj = namedtuple(
        "FormObj", "phillip_glasser_new summer_assignment_new",
    )
    return FormObj(
        phillip_glasser_new=phillip_glasser_new,
        summer_assignment_new=summer_assignment_new,
    )
