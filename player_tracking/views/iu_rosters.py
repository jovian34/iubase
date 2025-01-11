from datetime import date
from django import shortcuts, urls
from index import views as index_views
from player_tracking import choices
from player_tracking import models as pt_models


def fall(request, fall_year):
    if request.META.get("HTTP_HX_REQUEST"):
        return render_fall_roster_partial_template(request, fall_year)
    else:
        return shortcuts.redirect(urls.reverse("fall_players", args=[fall_year]))
    

def render_fall_roster_partial_template(request, fall_year):
    players = (pt_models.AnnualRoster.objects.filter(spring_year=int(fall_year) + 1)
        .filter(team__team_name="Indiana")
        .order_by("jersey")
    )
    context = {
        "fall_year": fall_year,
        "years": [int(fall_year) - 2 + i for i in range(5)],
        "players": players,
        "page_title": f"Fall {fall_year} Roster",
        "total": len(players),
    }
    template_path = "player_tracking/partials/roster.html"
    return shortcuts.render(request, template_path, context)


def spring(request, spring_year):
    players_for_year = (
        pt_models.AnnualRoster.objects.filter(spring_year=int(spring_year))
        .filter(team__team_name="Indiana")
        .filter(status__in=choices.ALL_ROSTER)
        .order_by("jersey")
    )
    context = {
        "players": players_for_year,
        "page_title": set_page_title_by_roster_status(spring_year, players_for_year),
        "total": len(players_for_year),
        "accolades": pt_models.Accolade.objects.filter(annual_roster__in=players_for_year),
    }
    index_views.save_traffic_data(request=request, page=context["page_title"])
    template_path = "player_tracking/roster.html"
    return shortcuts.render(request, template_path, context)


def set_page_title_by_roster_status(spring_year, players_for_year):
    if len(players_for_year) < 29 and int(spring_year) >= date.today().year:
        page_title = f"Spring {spring_year} Roster not fully announced"
    else:
        page_title = f"Spring {spring_year} Roster"
    return page_title
