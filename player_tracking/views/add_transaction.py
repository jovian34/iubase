from django.contrib.auth import decorators as auth
from django import http, shortcuts, urls

from player_tracking.forms import TransactionForm
from player_tracking.views.set_player_properties import set_player_props_get_errors
from player_tracking.models import Player, Transaction

from datetime import date


@auth.login_required
def view(request, player_id):
    if not request.user.has_perm("player_tracking.add_transaction"):
        return http.HttpResponseForbidden()
    elif request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            save_transaction_form(player_id, form)
            set_player_props_get_errors()
        return shortcuts.redirect(urls.reverse("single_player_page", args=[player_id]))
    else:
        form = TransactionForm(
            initial={
                "trans_date": date.today(),
            },
        )
        context = {
            "form": form,
            "player_id": player_id,
        }
        return shortcuts.render(
            request,
            "player_tracking/partials/add_transaction.html",
            context,
        )


def save_transaction_form(player_id, form):
    add_transaction = Transaction.objects.create(
        player=Player.objects.get(pk=player_id),
        trans_event=form.cleaned_data["trans_event"],
        trans_date=form.cleaned_data["trans_date"],
        citation=form.cleaned_data["citation"],
        primary_position=form.cleaned_data["primary_position"],
        other_team=form.cleaned_data["other_team"],
        prof_org=form.cleaned_data["prof_org"],
        draft_round=form.cleaned_data["draft_round"],
        bonus_or_slot=form.cleaned_data["bonus_or_slot"],
        comment=form.cleaned_data["comment"],
    )
    add_transaction.save()
