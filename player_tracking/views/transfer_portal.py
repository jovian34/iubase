from datetime import date

from django.shortcuts import render
from django.db.models.functions import Lower

from player_tracking.models import Transaction
from index.views import save_traffic_data


def view(request, portal_year):
    start = date(year=int(portal_year)-1, month=9, day=1)
    end = date(year=int(portal_year), month=8, day=31)
    outgoing = Transaction.objects.filter(
        trans_event="Entered Transfer Portal",
        trans_date__gte=start,
        trans_date__lte=end,
    ).order_by("player__last")
    incoming = Transaction.objects.filter(
        trans_event="Verbal Commitment from College",
        trans_date__gte=start,
        trans_date__lte=end,
    ).order_by(Lower("player__last"))
    context = {
        "outgoing": outgoing,
        "incoming": incoming,
        "page_title": f"{portal_year} Transfer Portal",
        "total_out": str(len(outgoing)),
        "total_in": str(len(incoming)),
        "portal_year": portal_year,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/portal.html", context)
