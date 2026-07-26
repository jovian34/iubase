from datetime import date

import pytest
from bs4 import BeautifulSoup
from django.contrib.auth.models import Permission
from django.urls import reverse

from accounts.tests.fixtures import logged_user_schwarbs
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.models import Transaction
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions


this_year = date.today().year


def grant_change_transaction_permission(user):
    permission = Permission.objects.get(
        content_type__app_label="player_tracking",
        codename="change_transaction",
    )
    user.user_permissions.add(permission)


def edited_transaction_data(team, prof_org):
    return {
        "trans_event": "National Letter of Intent Signed",
        "trans_date": date(this_year - 2, 11, 8),
        "citation": "https://example.com/updated-transaction",
        "primary_position": "First Base",
        "other_team": team.pk,
        "prof_org": prof_org.pk,
        "draft_round": 2,
        "bonus_or_slot": 500000,
        "comment": "Updated transaction details.",
    }


@pytest.mark.django_db
def test_player_page_omits_transaction_edit_buttons_without_permission(
    client,
    players,
    transactions,
    annual_rosters,
    logged_user_schwarbs,
):
    response = client.get(
        reverse("single_player_page", args=[players.devin_taylor.pk])
    )

    assert "edit transaction</button>" not in response.content.decode()


@pytest.mark.django_db
def test_player_page_renders_edit_button_after_each_transaction_with_permission(
    client,
    players,
    transactions,
    annual_rosters,
    logged_user_schwarbs,
):
    grant_change_transaction_permission(logged_user_schwarbs)
    response = client.get(
        reverse("single_player_page", args=[players.devin_taylor.pk])
    )
    transaction_section = BeautifulSoup(
        response.content,
        "html.parser",
    ).find(id="transactions")

    player_transactions = (
        transactions.dt_draft_ranked,
        transactions.dt_nli,
        transactions.dt_verbal,
    )
    for transaction in player_transactions:
        control_id = f"edit-transaction-{transaction.pk}-control"
        edit_control = transaction_section.find(id=control_id)
        assert edit_control is not None
        edit_button = edit_control.find("button", string="edit transaction")
        assert edit_button is not None
        assert edit_button["hx-get"] == reverse(
            "edit_transaction",
            args=[transaction.pk],
        )
        assert edit_button["hx-target"] == f"#{control_id}"

        transaction_record = edit_control.find_parent("li")
        transaction_elements = list(transaction_record.descendants)
        transaction_details = transaction_record.find("p")
        details_position = transaction_elements.index(transaction_details)
        control_position = transaction_elements.index(edit_control)
        assert details_position < control_position


@pytest.mark.django_db
def test_edit_transaction_form_forbidden_without_permission(
    client,
    transactions,
    logged_user_schwarbs,
):
    response = client.get(
        reverse("edit_transaction", args=[transactions.dt_verbal.pk])
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_transaction_form_renders_current_values_for_authorized_user(
    client,
    transactions,
    logged_user_schwarbs,
):
    grant_change_transaction_permission(logged_user_schwarbs)
    transaction = transactions.nm_draft
    form_url = reverse("edit_transaction", args=[transaction.pk])

    response = client.get(form_url, HTTP_HX_REQUEST="true")
    form = response.context["form"]
    rendered_form = BeautifulSoup(response.content, "html.parser").find("form")

    assert response.status_code == 200
    assert form.initial["trans_event"] == transaction.trans_event
    assert form.initial["trans_date"] == transaction.trans_date
    assert form.initial["citation"] == transaction.citation
    assert form.initial["primary_position"] == transaction.primary_position
    assert form.initial["other_team"] == transaction.other_team
    assert form.initial["prof_org"] == transaction.prof_org
    assert form.initial["draft_round"] == transaction.draft_round
    assert form.initial["bonus_or_slot"] == transaction.bonus_or_slot
    assert form.initial["comment"] == transaction.comment
    assert rendered_form["hx-post"] == form_url
    assert rendered_form["hx-target"] == "#transactions"


@pytest.mark.django_db
def test_edit_transaction_submission_forbidden_without_permission(
    client,
    transactions,
    teams,
    prof_orgs,
    logged_user_schwarbs,
):
    transaction = transactions.dt_verbal
    original_event = transaction.trans_event

    response = client.post(
        reverse("edit_transaction", args=[transaction.pk]),
        edited_transaction_data(teams.duke, prof_orgs.phillies),
        HTTP_HX_REQUEST="true",
    )
    transaction.refresh_from_db()

    assert response.status_code == 403
    assert transaction.trans_event == original_event
    assert transaction.comment is None


@pytest.mark.django_db
def test_authorized_edit_transaction_updates_and_renders_transaction_section(
    client,
    transactions,
    teams,
    prof_orgs,
    annual_rosters,
    logged_user_schwarbs,
):
    grant_change_transaction_permission(logged_user_schwarbs)
    transaction = transactions.dt_verbal

    response = client.post(
        reverse("edit_transaction", args=[transaction.pk]),
        edited_transaction_data(teams.duke, prof_orgs.phillies),
        HTTP_HX_REQUEST="true",
    )
    updated_transaction = Transaction.objects.get(pk=transaction.pk)
    output = response.content.decode()

    assert response.status_code == 200
    assert updated_transaction.trans_event == "National Letter of Intent Signed"
    assert updated_transaction.trans_date == date(this_year - 2, 11, 8)
    assert updated_transaction.citation == "https://example.com/updated-transaction"
    assert updated_transaction.primary_position == "First Base"
    assert updated_transaction.other_team == teams.duke
    assert updated_transaction.prof_org == prof_orgs.phillies
    assert updated_transaction.draft_round == 2
    assert updated_transaction.bonus_or_slot == 500000
    assert updated_transaction.comment == "Updated transaction details."
    assert 'id="transactions"' in output
    assert "National Letter of Intent Signed" in output
    assert "edit transaction</button>" in output
