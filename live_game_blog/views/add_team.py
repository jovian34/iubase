from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from live_game_blog.forms import AddTeamForm
from live_game_blog.models import Team


@login_required
def view(request):
    if request.method == "POST":
        form = AddTeamForm(request.POST)
        if form.is_valid():
            add_team = Team(
                team_name=form.cleaned_data["team_name"],
                mascot=form.cleaned_data["mascot"],
                logo=form.cleaned_data["logo"],
                stats=form.cleaned_data["stats"],
                roster=form.cleaned_data["roster"],
            )
            add_team.save()
        return redirect(reverse("games"))
    else:
        form = AddTeamForm()
        context = {
            "form": form,
            "page_title": "Add Team",
        }
        return render(request, "live_game_blog/add_team.html", context)
