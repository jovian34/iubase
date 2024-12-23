from django import shortcuts

from player_tracking import forms

def view(request, player_id):
    context = {
        "player_id": player_id,
        "form": forms.AccoladeForm(),
    }
    return shortcuts.render(
        request,
        "player_tracking/partials/add_accolade.html",
        context,
    )