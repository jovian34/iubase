from django import http, shortcuts
from django.contrib.auth import decorators as auth

from player_tracking.forms import TransactionForm
from player_tracking.models import Transaction
from player_tracking.views import set_player_properties, single_player_page


@auth.login_required
def view(request, transaction_id):
    if not request.user.has_perm("player_tracking.change_transaction"):
        return http.HttpResponseForbidden()
    if not single_player_page.is_htmx_request(request):
        return http.HttpResponseBadRequest()

    transaction = shortcuts.get_object_or_404(Transaction, pk=transaction_id)
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            update_transaction_from_form(transaction, form)
            return render_updated_transactions(request, transaction)
    else:
        form = initialize_transaction_form(transaction)

    context = {
        "form": form,
        "transaction": transaction,
    }
    return shortcuts.render(
        request,
        "player_tracking/partials/edit_transaction.html",
        context,
    )


def initialize_transaction_form(transaction):
    return TransactionForm(
        initial={
            "trans_event": transaction.trans_event,
            "trans_date": transaction.trans_date,
            "citation": transaction.citation,
            "primary_position": transaction.primary_position,
            "other_team": transaction.other_team,
            "prof_org": transaction.prof_org,
            "draft_round": transaction.draft_round,
            "bonus_or_slot": transaction.bonus_or_slot,
            "comment": transaction.comment,
        }
    )


def update_transaction_from_form(transaction, form):
    transaction.trans_event = form.cleaned_data["trans_event"]
    transaction.trans_date = form.cleaned_data["trans_date"]
    transaction.citation = form.cleaned_data["citation"]
    transaction.primary_position = form.cleaned_data["primary_position"]
    transaction.other_team = form.cleaned_data["other_team"]
    transaction.prof_org = form.cleaned_data["prof_org"]
    transaction.draft_round = form.cleaned_data["draft_round"]
    transaction.bonus_or_slot = form.cleaned_data["bonus_or_slot"]
    transaction.comment = form.cleaned_data["comment"]
    transaction.save()
    set_player_properties.set_player_props_get_errors()


def render_updated_transactions(request, transaction):
    return single_player_page.render_player_section(
        request,
        transaction.player_id,
        "player_tracking/partials/player_transactions.html",
    )
