from django.db import transaction
from live_game_blog.models import Team
from player_tracking import models as pt_models


@transaction.atomic
def save_roster_entries(formset, players, spring_year):
    projected_players = {player.pk: player for player in players}
    team = Team.objects.get(team_name="Indiana")
    for form in formset:
        if not form.cleaned_data or form.cleaned_data.get("jersey") is None:
            continue
        player = projected_players[form.cleaned_data["player"]]
        if pt_models.AnnualRoster.objects.filter(
            player=player, spring_year=spring_year
        ).exists():
            continue
        pt_models.AnnualRoster.objects.create(
            spring_year=spring_year,
            team=team,
            player=player,
            jersey=form.cleaned_data["jersey"],
            status="Fall Roster",
            primary_position=form.cleaned_data["primary_position"],
        )