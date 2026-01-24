from decimal import Decimal
from django import shortcuts
from conference.logic import resolve_ties, get_standings_data
from conference import models as conf_models


def view(request, spring_year):
    teams_qs = get_standings_data.annotated_teams_queryset(spring_year)
    teams_qs = get_standings_data.limit_to_teams_with_B1G_rpi_and_games_this_season(
        teams_qs
    )
    teams_list = create_teams_list_from_queryset(teams_qs)
    ordered = resolve_ties.resolve_ties(teams_list, spring_year)
    ordered_for_template = create_ordered_standings_for_use_in_template(ordered)
    b1g = conf_models.Conference.objects.get(abbrev="B1G")
    template_path = "conference/standings.html"
    context = {
        "page_title": f"{spring_year} B1G Standings",
        "standings": ordered_for_template,
        "spring_year": spring_year,
        "B1G": b1g,
    }
    return shortcuts.render(request, template_path, context)


def create_teams_list_from_queryset(teams_qs):
    teams_list = []
    for team in teams_qs:
        teams_list.append(
            {
                "pk": team.pk,
                "team_name": team.team_name,
                "wins": Decimal(team.wins),
                "losses": Decimal(team.losses),
                "win_pct": float(team.win_pct or 0.0),
                "rpi_rank": int(team.rpi_rank) if team.rpi_rank is not None else None,
                "obj": team,
                "tiebreaker": None,
            }
        )
    return teams_list


def create_ordered_standings_for_use_in_template(ordered):
    ordered_for_template = []
    for pos, entry in enumerate(ordered, start=1):
        model_obj = entry.get("obj")
        model_obj.computed_wins = entry["wins"]
        model_obj.computed_losses = entry["losses"]
        model_obj.computed_win_pct = entry["win_pct"]
        model_obj.computed_rpi_rank = entry["rpi_rank"]
        model_obj.standings_position = pos
        model_obj.tie_breaker = entry.get("tiebreaker")
        ordered_for_template.append(model_obj)
    return ordered_for_template
