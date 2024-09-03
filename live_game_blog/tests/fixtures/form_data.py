import pytest

from collections import namedtuple

from live_game_blog.tests.fixtures.teams import teams


@pytest.fixture
def forms(teams):
    pfw = {
        "team_name": "Purdue Ft. Wayne",
        "mascot": "Mastodons",
        "logo": "https://cdn.d1baseball.com/uploads/2023/12/21143914/iupufw.png",
        "stats": "https://d1baseball.com/team/iupufw/stats/",
        "roster": "https://gomastodons.com/sports/baseball/roster",
    }
    iu_v_gm = {
        "home_team": [str(teams.indiana.pk)],
        "away_team": [str(teams.gm.pk)],
        "neutral_site": ["on"],
        "live_stats": [
            "https://stats.statbroadcast.com/broadcast/?id=491945&vislive=ind"
        ],
        "first_pitch": ["2025-02-14-1830"],
    }
    iu_holds_duke = {
        "game_status": "in-progress",
        "inning_num": "2",
        "inning_part": "Bottom",
        "outs": "3",
        "home_runs": "1",
        "away_runs": "3",
        "home_hits": "2",
        "away_hits": "5",
        "home_errors": "1",
        "away_errors": "0",
        "blog_entry": "Indiana holds Duke to one run",
    }
    iu_slams_duke = {
        "game_status": "in-progress",
        "inning_num": "4",
        "inning_part": "Top",
        "outs": "1",
        "home_runs": "1",
        "away_runs": "7",
        "home_hits": "2",
        "away_hits": "9",
        "home_errors": "1",
        "away_errors": "0",
        "blog_entry": "## DEVIN TAYLOR SALAMI!!!!",
    }
    uk_tourney = {
        "home_team": [str(teams.kentucky.pk)],
        "home_rank": ["20"],
        "home_seed": ["1"],
        "home_nat_seed": ["14"],
        "away_team": [str(teams.indiana.pk)],
        "away_seed": ["3"],
        "live_stats": [
            "https://stats.statbroadcast.com/broadcast/?id=491945&vislive=ind"
        ],
        "first_pitch": ["2025-06-03-1800"],
    }
    FormObj = namedtuple(
        "FormObj",
        "pfw iu_v_gm iu_holds_duke iu_slams_duke uk_tourney",
    )
    return FormObj(
        pfw=pfw,
        iu_v_gm=iu_v_gm,
        iu_holds_duke=iu_holds_duke,
        iu_slams_duke=iu_slams_duke,
        uk_tourney=uk_tourney,
    )