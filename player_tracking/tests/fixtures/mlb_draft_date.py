import pytest

from collections import namedtuple
from datetime import date, timedelta

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
def very_soon_mlb_draft_date():
    draft_soon = MLBDraftDate.objects.create(
        fall_year=this_year,
        latest_birthdate=date.today() - timedelta(days=7671),
        latest_draft_day=date.today() + timedelta(days=1),
        signing_deadline=date.today() + timedelta(days=22),
    )
    MLBDraftDateObj = namedtuple("MLBDraftDateObj", "draft_soon")
    return MLBDraftDateObj(
        draft_soon=draft_soon,
    )


@pytest.fixture
def past_mlb_draft_date():
    draft_past = MLBDraftDate.objects.create(
        fall_year=this_year,
        latest_birthdate=date.today() - timedelta(days=7700),
        latest_draft_day=date.today() - timedelta(days=22),
        signing_deadline=date.today() - timedelta(days=1),
    )
    MLBDraftDateObj = namedtuple("MLBDraftDateObj", "draft_past")
    return MLBDraftDateObj(
        draft_past=draft_past,
    )


@pytest.fixture
def today_complete_mlb_draft_date():
    draft_complete_today = MLBDraftDate.objects.create(
        fall_year=this_year,
        latest_birthdate=date.today() - timedelta(days=7690),
        latest_draft_day=date.today(),
        signing_deadline=date.today() + timedelta(days=22),
        draft_complete=True,
    )
    MLBDraftDateObj = namedtuple("MLBDraftDateObj", "draft_complete_today")
    return MLBDraftDateObj(
        draft_complete_today=draft_complete_today,
    )


@pytest.fixture
def today_incomplete_mlb_draft_date():
    draft_incomplete_today = MLBDraftDate.objects.create(
        fall_year=this_year,
        latest_birthdate=date.today() - timedelta(days=7690),
        latest_draft_day=date.today(),
        signing_deadline=date.today() + timedelta(days=22),
    )
    MLBDraftDateObj = namedtuple("MLBDraftDateObj", "draft_incomplete_today")
    return MLBDraftDateObj(
        draft_incomplete_today=draft_incomplete_today,
    )