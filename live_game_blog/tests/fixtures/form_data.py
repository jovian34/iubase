import pytest

from collections import namedtuple
from django.utils import timezone
import datetime

from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs


@pytest.fixture
def forms(teams, stadiums, stadium_configs):
    pfw = {
        "team_name": "Purdue Ft. Wayne",
        "mascot": "Mastodons",
        "logo": "https://cdn.d1baseball.com/uploads/2023/12/21143914/iupufw.png",
        "stats": "https://d1baseball.com/team/iupufw/stats/",
        "roster": "https://gomastodons.com/sports/baseball/roster",
        "stadium_config": [str(stadium_configs.bart.pk)]
    }
    iu_v_gm = {
        "home_team": [str(teams.indiana.pk)],
        "away_team": [str(teams.gm.pk)],
        "live_stats": [
            "https://stats.statbroadcast.com/broadcast/?id=491945&vislive=ind"
        ],
        "first_pitch": ["2025-02-14-1830"],
        "stadium_config": [str(stadium_configs.surprise.pk)]
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
    edit_blog_uk_wins = {
        "blog_entry": "Kentucky moves on to Super Regionals",
        "game_status": "final",
        "inning_num": "9",
        "inning_part": "Top",
        "outs": "3",
        "home_runs": "4",
        "away_runs": "2",
        "home_hits": "7",
        "away_hits": "10",
        "home_errors": "1",
        "away_errors": "2",
    }
    edit_iu_coastal_ip = {
        "home_team": [str(teams.coastal.pk)],
        "away_team": [str(teams.indiana.pk)],
        "first_pitch": (timezone.now() - datetime.timedelta(hours=1)),
        "event": ["Baseball at the Beach"],
    }
    unc_stadium = {
        "address": "235 Ridge Rd.",
        "city": "Chapel Hill",
        "state": "NC",
        "country": "USA",
        "timezone": "America/New_York",
        "lat": "35.90630",
        "long": "-79.04304",
        "stadium_name": "Bryson Field at Boshamer Stadium",
        "config_date": "2009-02-02",
        "designate_date": "2009-02-02",
        "surface_inf": "natural",
        "surface_out": "natural",
        "surface_mound": "natural",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Cary_C._Boshamer_Stadium.JPG/250px-Cary_C._Boshamer_Stadium.JPG",
        "capacity": "5000",
        "orientation": "194",
        "left": "335",
        "center": "400",
        "right": "340",
        "lights": "on",
        "home_dugout": "third",
    }
    FormObj = namedtuple(
        "FormObj",
        "pfw iu_v_gm iu_holds_duke iu_slams_duke uk_tourney edit_blog_uk_wins edit_iu_coastal_ip unc_stadium",
    )
    return FormObj(
        pfw=pfw,
        iu_v_gm=iu_v_gm,
        iu_holds_duke=iu_holds_duke,
        iu_slams_duke=iu_slams_duke,
        uk_tourney=uk_tourney,
        edit_blog_uk_wins=edit_blog_uk_wins,
        edit_iu_coastal_ip=edit_iu_coastal_ip,
        unc_stadium=unc_stadium,
    )
