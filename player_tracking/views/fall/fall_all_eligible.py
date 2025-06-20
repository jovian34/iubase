from django.shortcuts import render, redirect
from django.db.models.functions import Lower
from player_tracking.models import Player, MLBDraftDate


def view(request, fall_year):
    if request.META.get("HTTP_HX_REQUEST"):
        spring_year = int(fall_year) + 1
        players = (
            Player.objects.filter(first_spring__lte=spring_year)
            .filter(last_spring__gte=spring_year)
            .order_by(Lower("last"))
        )
        draft_year = True
        try:
            draft_complete = MLBDraftDate.objects.get(
                fall_year=int(fall_year)
            ).draft_complete
        except MLBDraftDate.DoesNotExist:
            draft_year, draft_complete = False, False
        context = {
            "fall_year": fall_year,
            "years": [int(fall_year) - 2 + i for i in range(5)],
            "players": players,
            "page_title": f"All Eligible Players For Fall {fall_year}",
            "count": len(players),
            "draft_year": draft_year,
            "draft_complete": draft_complete,
        }
        return render(
            request, "player_tracking/partials/all_eligible_players_fall.html", context
        )
    else:
        return redirect("fall_players", fall_year=fall_year)
