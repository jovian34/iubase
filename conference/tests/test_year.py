import datetime

import pytest

from conference.logic import year


@pytest.mark.parametrize(
    ("today", "expected_spring_year"),
    (
        (datetime.date(2026, 8, 31), 2026),
        (datetime.date(2026, 9, 1), 2027),
    ),
)
def test_get_spring_year_uses_september_as_season_boundary(
    monkeypatch,
    today,
    expected_spring_year,
):
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return today

    monkeypatch.setattr(year.datetime, "date", FixedDate)

    assert year.get_spring_year() == expected_spring_year
