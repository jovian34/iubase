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
    FormObj = namedtuple(
        "FormObj",
        "pfw iu_v_gm",
    )
    return FormObj(
        pfw=pfw,
        iu_v_gm=iu_v_gm,
    )