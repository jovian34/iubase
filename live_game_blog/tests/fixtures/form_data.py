import pytest

from collections import namedtuple
from django.utils import timezone
import datetime

from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.stadiums import stadiums


@pytest.fixture
def forms(teams, stadiums):
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
        "live_stats": [
            "https://stats.statbroadcast.com/broadcast/?id=491945&vislive=ind"
        ],
        "first_pitch": ["2025-02-14-1830"],
        "stadium": [str(stadiums.surprise.pk)]
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
        "first_pitch_wind_direction": "ENE",
        "event": ["Baseball at the Beach"],
    }
    uk_stadium = {
        "address": ["510 Wildcat Ct."],
        "city": ["Lexington"],
        "state": ["Kentucky"],
        "country": ["USA"],
        "timezone": ["America/New_York"],
        "lat": ["38.01822"],
        "long": ["-84.50317"],
        "stadium_name": ["Kentucky Proud Park"],
        "config_date": ["2019-01-01"],
        "designate_date": ["2019-02-15"],
        "surface_inf": ["artificial"],
        "surface_out": ["artificial"],
        "surface_mound": ["artificial"],
        "photo": ["https://live.staticflickr.com/65535/52947179552_349321280b_c.jpg"],
        "capacity": ["7000"],
        "orientation": ["100"],
        "left": ["335"],
        "center": ["400"],
        "right": ["320"],
        "lights": ["on"],
        "home_dugout": ["left"],
    }
    FormObj = namedtuple(
        "FormObj",
        "pfw iu_v_gm iu_holds_duke iu_slams_duke uk_tourney edit_blog_uk_wins edit_iu_coastal_ip uk_stadium",
    )
    return FormObj(
        pfw=pfw,
        iu_v_gm=iu_v_gm,
        iu_holds_duke=iu_holds_duke,
        iu_slams_duke=iu_slams_duke,
        uk_tourney=uk_tourney,
        edit_blog_uk_wins=edit_blog_uk_wins,
        edit_iu_coastal_ip=edit_iu_coastal_ip,
        uk_stadium=uk_stadium,
    )
