from datetime import date

from django.db.models.functions import Lower
from django.shortcuts import render

from index.views import save_traffic_data
from player_tracking.models import Transaction


def view(request, portal_year):
    if not 1900 <= portal_year <= date.today().year + 1:
        from django.http import Http404

        raise Http404("Transfer portal year is outside the supported range")

    start = date(year=portal_year - 1, month=9, day=1)
    end = date(year=portal_year, month=8, day=31)
    outgoing = Transaction.objects.filter(
        trans_event="Entered Transfer Portal",
        trans_date__gte=start,
        trans_date__lte=end,
    ).order_by("player__last")
    outgoing_commit = Transaction.objects.filter(
        trans_event="Verbal Commitment to Transfer College",
        trans_date__gte=start,
        trans_date__lte=end,
    )
    incoming = Transaction.objects.filter(
        trans_event="Verbal Commitment from College",
        trans_date__gte=start,
        trans_date__lte=end,
    ).order_by(Lower("player__last"))
    context = {
        "outgoing": outgoing,
        "outgoing_commit": outgoing_commit,
        "incoming": incoming,
        "page_title": f"{portal_year} Transfer Portal",
        "total_out": str(len(outgoing)),
        "total_in": str(len(incoming)),
        "portal_year": portal_year,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/portal.html", context)
