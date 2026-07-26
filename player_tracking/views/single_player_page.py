from django.shortcuts import render
from django import http


from player_tracking.models import (
    Player,
    Transaction,
    AnnualRoster,
    SummerAssign,
    Accolade,
)
from index.views import save_traffic_data


def view(request, player_id):
    context = get_player_context(player_id)
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/single_player_page.html", context)


def render_player_section(request, player_id, template_name):
    context = get_player_context(player_id)
    return render(request, template_name, context)


def get_player_context(player_id):
    player = get_player(player_id)
    return {
        "player": player,
        "page_title": f"{player.first} {player.last}",
        "rosters": AnnualRoster.objects.filter(player=player).order_by("-spring_year"),
        "transactions": Transaction.objects.filter(player=player).order_by(
            "-trans_date"
        ),
        "summers": SummerAssign.objects.filter(player=player).order_by("-summer_year"),
        "accolades": Accolade.objects.filter(player=player).order_by("-award_date"),
    }


def get_player(player_id):
    try:
        return Player.objects.get(pk=player_id)
    except Player.DoesNotExist:
        raise http.Http404


def is_htmx_request(request):
    return bool(request.META.get("HTTP_HX_REQUEST"))
