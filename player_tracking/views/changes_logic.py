from player_tracking.models import Player, Transaction

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