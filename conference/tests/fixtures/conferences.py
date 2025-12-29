import pytest
from collections import namedtuple

from conference import models as conf_models



@pytest.fixture
def conferences(client):
    b1g = conf_models.Conference.objects.create(
        abbrev = "B1G",
        long_name = "Big Ten Conference",
        logo_url = "https://cdn.d1baseball.com/uploads/2023/12/21135509/big-ten-conference.png",
    )
    sec = conf_models.Conference.objects.create(
        abbrev = "SEC",
        long_name = "Southeastern Conference",
        logo_url = "https://cdn.d1baseball.com/uploads/2023/12/21135542/southeastern-conference.png"
    )
    p10 = conf_models.Conference.objects.create(
        abbrev = "Pac 10",
        long_name = "Pacific-10 Conference",
        logo_url = "https://content.sportslogos.net/logos/153/4945/full/pacific-10_conference_logo_primary_19956829.png"
    )
    p12 = conf_models.Conference.objects.create(
        abbrev = "Pac 12",
        long_name = "Pacific-12 Conference",
        logo_url = "https://upload.wikimedia.org/wikipedia/en/thumb/a/ac/Pac-12_logo.svg/150px-Pac-12_logo.svg.png"
    )
    hor = conf_models.Conference.objects.create(
        abbrev = "HOR",
        long_name = "Horizon League",
        logo_url = "https://cdn.d1baseball.com/uploads/2023/12/21135517/horizon-league.png",
    )
    non_d1 = conf_models.Conference.objects.create(
        abbrev = "nonD1",
        long_name = "Not in NCAA Division I",
        logo_url = "https://seeklogo.com/images/B/baseball-logo-8DD18EC9B4-seeklogo.com.png",
    )
    ConfObj = namedtuple(
        "ConfObj",
        "b1g sec p10 p12 hor non_d1",
    )
    return ConfObj(
        b1g=b1g,
        sec=sec,
        p10=p10,
        p12=p12,
        hor=hor,
        non_d1=non_d1,
    )