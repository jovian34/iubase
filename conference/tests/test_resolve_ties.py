from datetime import date
from decimal import Decimal

import pytest

from conference import models as conf_models
from conference.logic import resolve_ties
from live_game_blog.tests.fixtures.teams import teams


SPRING_YEAR = 2026


def create_series(home_team, away_team, home_wins, away_wins):
    return conf_models.ConfSeries.objects.create(
        home_team=home_team,
        away_team=away_team,
        home_wins=home_wins,
        away_wins=away_wins,
        start_date=date(SPRING_YEAR, 3, 6),
    )


def tied_team(team, rpi_rank):
    return {
        "pk": team.pk,
        "team_name": team.team_name,
        "win_pct": 0.500,
        "rpi_rank": rpi_rank,
    }


@pytest.mark.django_db
def test_head_to_head_recursively_resolves_remaining_tied_teams(teams):
    create_series(teams.indiana, teams.iowa, 2, 1)
    create_series(teams.indiana, teams.ucla, 2, 1)
    create_series(
        teams.iowa,
        teams.ucla,
        Decimal("1.5"),
        Decimal("1.5"),
    )
    tied_teams = [
        tied_team(teams.indiana, 100),
        tied_team(teams.iowa, 20),
        tied_team(teams.ucla, 30),
    ]

    resolved = resolve_ties.resolve_ties(tied_teams, SPRING_YEAR)

    assert [team["team_name"] for team in resolved] == [
        "Indiana",
        "Iowa",
        "UCLA",
    ]
    assert resolved[0]["tiebreaker"] == "tie broke by head-to-head"
    assert resolved[1]["tiebreaker"] == "tie broken by RPI"
    assert resolved[2]["tiebreaker"] == "tie broken by RPI"


@pytest.mark.django_db
def test_rpi_resolves_tie_when_no_prior_tiebreaker_applies(teams):
    tied_teams = [
        tied_team(teams.indiana, 25),
        tied_team(teams.iowa, None),
        tied_team(teams.ucla, 5),
    ]

    resolved = resolve_ties.resolve_ties(tied_teams, SPRING_YEAR)

    assert [team["team_name"] for team in resolved] == [
        "UCLA",
        "Indiana",
        "Iowa",
    ]
    assert all(team["tiebreaker"] == "tie broke by RPI" for team in resolved)
