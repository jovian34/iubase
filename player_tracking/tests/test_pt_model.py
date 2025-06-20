import pytest
from datetime import date, timedelta

from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.summer import (
    summer_leagues,
    summer_teams,
    summer_assign,
)
from player_tracking.tests.fixtures.accolades import accolades
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from live_game_blog.tests.fixtures.teams import teams

this_year = date.today().year


@pytest.mark.django_db
def test_player_model_string_def(players):
    assert str(players.devin_taylor) == f"Devin Taylor {this_year - 2}"


@pytest.mark.django_db
def test_transaction_model_string_def(transactions):
    assert (
        str(transactions.dt_verbal)
        == f"Devin Taylor Verbal Commitment from High School on March {this_year - 3}"
    )


@pytest.mark.django_db
def test_mlb_draft_birthdate_string_def(typical_mlb_draft_date):
    assert (
        str(typical_mlb_draft_date.draft_this_year)
        == f"{this_year}: Aug 1, {this_year - 21}"
    )


@pytest.mark.django_db
def test_summer_assign_string_def(summer_assign):
    assert str(summer_assign.dt_usa_ty) == f"Devin Taylor {this_year} USA"


@pytest.mark.django_db
def test_accolade_model_str_def(accolades, annual_rosters, teams):
    award_date = date.today() - timedelta(days=60)
    assert (
        str(accolades.dt_ly_b1g_first_team)
        == f"Devin Taylor {award_date.year} B1G First Team All-Conference Outfielder"
    )
