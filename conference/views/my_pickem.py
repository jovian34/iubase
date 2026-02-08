import datetime

from django import shortcuts, urls
from django.contrib.auth import decorators as auth
from django.db.models import Q

from conference import models as conf_models


@auth.login_required
def view(request, spring_year):
    registration = conf_models.PickemRegisterAnnual.objects.filter(
        user=request.user,
        spring_year=spring_year,
    ).first()
    if not registration:
        return shortcuts.redirect(urls.reverse("pickem_register", args=[spring_year]))
    
    prior_series = conf_models.ConfSeries.objects.filter(
        Q(start_date__lte=datetime.date.today()) &
        Q(start_date__gt=datetime.date(year=int(spring_year), month=2, day=1))
    ).order_by("-start_date")
    if prior_series.exists():
        current_week_series = conf_models.ConfSeries.objects.filter(
            start_date=prior_series[0].start_date,
        )
        current_week_picks = conf_models.Pick.objects.filter(
            series__start_date=prior_series[0].start_date,
            user=registration,
        )
    else:
        current_week_series, current_week_picks = None, None
    
    next_series = conf_models.ConfSeries.objects.filter(
        Q(start_date__gt=datetime.date.today()) &
        Q(start_date__lt=datetime.date(year=int(spring_year), month=8, day=1))
    ).order_by("start_date")
    if next_series.exists():
        next_week_series = conf_models.ConfSeries.objects.filter(
            start_date=next_series[0].start_date,
        )
        next_week_picks = conf_models.Pick.objects.filter(
            series__start_date=next_series[0].start_date,
            user=registration,
        )
    else:
        next_week_series, next_week_picks = None, None
        
    content = {
        "current_week_series": current_week_series,
        "current_week_picks": current_week_picks,
        "next_week_series": next_week_series,
        "next_week_picks": next_week_picks,
        "page_title": f"My {spring_year} Pick'em"
    }
    template_path = "conference/my_pickem.html"
    return shortcuts.render(request, template_path, content)