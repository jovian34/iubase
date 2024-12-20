import pytest
from datetime import date

from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.summer import (
    summer_leagues,
    summer_teams,
    summer_assign,
)

this_year = date.today().year


@pytest.mark.django_db
def test_transaction_model_string_def(client, transactions):
    assert (
        str(transactions.dt_verbal)
        == f"Devin Taylor Verbal Commitment from High School on March {this_year - 3}"
    )


@pytest.mark.django_db
def test_mlb_draft_birthdate_string_def(client, typical_mlb_draft_date):
    assert (
        str(typical_mlb_draft_date.draft_this_year) == f"{this_year}: Aug 1, {this_year - 21}"
    )


@pytest.mark.django_db
def test_summer_assign_string_def(client, summer_assign):
    assert str(summer_assign.dt_usa_2024) == f"Devin Taylor {this_year} USA"
