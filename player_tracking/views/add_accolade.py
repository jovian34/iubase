from django import shortcuts
from django import urls
from django.contrib.auth import decorators as auth_dec

from player_tracking import forms
from player_tracking.models import Accolade, AnnualRoster, Player


@auth_dec.login_required
def view(request, player_id):
    if request.method == "POST":
        form = forms.AccoladeForm(player_id=player_id, data=request.POST)
        if form.is_valid():
            create_accolade_and_save(player_id, form)
        return shortcuts.redirect(urls.reverse("single_player_page", args=[player_id]))
    else:
        context = {
            "player_id": player_id,
            "form": forms.AccoladeForm(player_id=player_id),
        }
        return shortcuts.render(
            request,
            "player_tracking/partials/add_accolade.html",
            context,
        )
    

def create_accolade_and_save(player_id, form):
    add_accolade = Accolade.objects.create(
                player=Player.objects.get(pk=player_id),
                name=form.cleaned_data["name"],
                award_date=form.cleaned_data["award_date"],
                award_org=form.cleaned_data["award_org"],
                description=form.cleaned_data["description"],
                citation=form.cleaned_data["citation"],
                annual_roster=form.cleaned_data["annual_roster"],
                summer_assign=form.cleaned_data["summer_assign"]
            )
    add_accolade.save()