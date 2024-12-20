import pytest

from collections import namedtuple
from datetime import date

from player_tracking.models import MLBDraftDate


this_year = date.today().year


@pytest.fixture
def typical_mlb_draft_date():
    draft_this_year = MLBDraftDate.objects.create(
        fall_year=this_year,
        latest_birthdate=date(this_year - 21, 8, 1),
        latest_draft_day=date(this_year, 7, 16),
        signing_deadline=date(this_year, 7, 25),
    )
    MLBDraftDateObj = namedtuple("MLBDraftDateObj", "draft_this_year")
    return MLBDraftDateObj(
        draft_this_year=draft_this_year,
    )


@pytest.fixture
def last_year_mlb_draft_date():
    draft_last_year = MLBDraftDate.objects.create(
        fall_year=this_year - 1,
        latest_birthdate=date(this_year - 22, 8, 1),
        latest_draft_day=date(this_year - 1, 7, 16),
        signing_deadline=date(this_year - 1, 7, 25),
    )
    MLBDraftDateObj = namedtuple("MLBDraftDateObj", "draft_last_year")
    return MLBDraftDateObj(
        draft_last_year=draft_last_year,
    )