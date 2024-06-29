import pytest

from collections import namedtuple
from datetime import date

from player_tracking.models import MLBDraftDate


@pytest.fixture
def mlb_draft_date():
    draft_2024 = MLBDraftDate.objects.create(
        fall_year=2024,
        latest_birthdate=date(2003, 8, 1),
        latest_draft_day=date(2024, 7, 16),
        signing_deadline=date(2024, 7, 25),
    )
    MLBDraftDateObj = namedtuple("MLBDraftDateObj", "draft_2024")
    return MLBDraftDateObj(
        draft_2024=draft_2024,
    )
