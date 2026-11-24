from django.shortcuts import redirect, render

from player_tracking.logic import projection


def projected_depth(request, fall_year):
    if request.META.get("HTTP_HX_REQUEST"):
        context = projection.set_projected_players(fall_year)
        return render(
            request,
            "player_tracking/partials/projected_players_fall_depth.html",
            context,
        )
    else:
        return redirect("fall_players", fall_year=fall_year)


def projected_alpha(request, fall_year):
    if request.META.get("HTTP_HX_REQUEST"):
        context = projection.set_projected_players(fall_year)
        return render(
            request,
            "player_tracking/partials/projected_players_fall_alpha.html",
            context,
        )
    else:
        return redirect("fall_players", fall_year=fall_year)
