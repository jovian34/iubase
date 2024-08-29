import pytest
from collections import namedtuple

from player_tracking.models import ProfOrg


@pytest.fixture
def prof_orgs():
    phillies = ProfOrg.objects.create(
        city="Philadelphia",
        mascot="Phillies",
    )
    d_backs = ProfOrg.objects.create(
        city="Arizona",
        mascot="Diamondbacks",
    )
    braves = ProfOrg.objects.create(
        city="Atlanta",
        mascot="Braves",
    )
    ProfOrgObj = namedtuple(
        "ProfOrgObj",
        "phillies d_backs braves",
    )
    return ProfOrgObj(
        phillies=phillies,
        d_backs=d_backs,
        braves=braves,
    )
