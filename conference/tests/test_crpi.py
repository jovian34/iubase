from datetime import date
from decimal import Decimal

import pytest

from conference import models as conf_models
from conference.logic import crpi
from live_game_blog.tests.fixtures.teams import teams


def get_row_for_team(rows, team):
    return next(row for row in rows if row["team"] == team)


@pytest.mark.django_db
def test_crpi_ignores_unplayed_and_nonconference_series(teams):
    spring_year = 2026
    conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.iowa,
        home_wins=2,
        away_wins=1,
        start_date=date(spring_year, 3, 6),
    )
    conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.ucla,
        start_date=date(spring_year, 3, 13),
    )
    conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.kentucky,
        home_wins=0,
        away_wins=3,
        start_date=date(spring_year, 3, 20),
    )

    rows = crpi.build_crpi_rows(
        [teams.indiana, teams.iowa, teams.ucla],
        spring_year,
    )
    indiana = get_row_for_team(rows, teams.indiana)
    iowa = get_row_for_team(rows, teams.iowa)
    ucla = get_row_for_team(rows, teams.ucla)

    assert indiana["conference_wins"] == Decimal("2")
    assert indiana["conference_losses"] == Decimal("1")
    assert iowa["conference_wins"] == Decimal("1")
    assert iowa["conference_losses"] == Decimal("2")
    assert ucla["conference_wins"] == Decimal("0")
    assert ucla["conference_losses"] == Decimal("0")
    assert ucla["conference_win_pct"] == Decimal("0")
    assert ucla["crpi"] == Decimal("0")
