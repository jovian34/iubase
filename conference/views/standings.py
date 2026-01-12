from decimal import Decimal

from django import shortcuts
from django.db.models import Q
from conference.views import resolve_ties_logic


def view(request, spring_year):
    teams_qs = resolve_ties_logic.annotated_teams_queryset(spring_year)
    teams_qs = limit_to_teams_with_B1G_rpi_and_games_this_season(teams_qs)    
    teams_list = create_teams_list_from_queryset(teams_qs)
    ordered = resolve_ties_logic.resolve_ties(teams_list, spring_year)
    ordered_for_template = create_ordered_standings_for_use_in_template(ordered)
    template_path = "conference/standings.html"
    context = {
        "page_title": f"{spring_year} B1G Standings",
        "standings": ordered_for_template,
        "spring_year": spring_year
    }
    return shortcuts.render(request, template_path, context)


def limit_to_teams_with_B1G_rpi_and_games_this_season(teams_qs):
    teams_qs = teams_qs.filter(
        rpi_rank__isnull=False
    ).filter(
        Q(wins__gt=0) | Q(losses__gt=0)
    )    
    return teams_qs


def create_teams_list_from_queryset(teams_qs):
    teams_list = []
    for t in teams_qs:
        teams_list.append({
            'pk': t.pk,
            'team_name': t.team_name,
            'wins': Decimal(t.wins),
            'losses': Decimal(t.losses),
            'win_pct': float(t.win_pct or 0.0),
            'rpi_rank': int(t.rpi_rank) if t.rpi_rank is not None else None,
            'obj': t,  # keep original model obj for rendering convenience
            'tiebreaker': None,
        })        
    return teams_list


def create_ordered_standings_for_use_in_template(ordered):
    ordered_for_template = []
    for pos, entry in enumerate(ordered, start=1):
        model_obj = entry.get('obj')
        # annotate some attributes the template expects
        model_obj.computed_wins = entry['wins']
        model_obj.computed_losses = entry['losses']
        model_obj.computed_win_pct = entry['win_pct']
        model_obj.computed_rpi_rank = entry['rpi_rank']
        model_obj.standings_position = pos
        # attach the tiebreaker string (None if not applicable)
        model_obj.tie_breaker = entry.get('tiebreaker')
        ordered_for_template.append(model_obj)
    return ordered_for_template
