import pytest
from collections import namedtuple

from conference import models as conf_models



@pytest.fixture
def conferences(client):
    b1g = conf_models.Conference.objects.create(
        abbrev = "B1G",
        long_name = "Big Ten Conference",
    )
    sec = conf_models.Conference.objects.create(
        abbrev = "SEC",
        long_name = "Southeastern Conference",
    )
    ConfObj = namedtuple(
        "ConfObj",
        "b1g sec",
    )
    return ConfObj(
        b1g=b1g,
        sec=sec,
    )