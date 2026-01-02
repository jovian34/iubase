import datetime

from django import shortcuts
from django.db.models import Q
from conference import year

from conference import models as conf_models


def view(request, spring_year):
    all_series = conf_models.ConfSeries.objects.filter(
        Q(start_date__gt=datetime.date(int(spring_year),1,1)) & Q(start_date__lt=datetime.date(int(spring_year),7,1))
    ).order_by("away_team__team_name")
    start_dates = { series.start_date for series in all_series }
    print(start_dates)
    start_dates = [ date for date in start_dates]
    start_dates.sort()
    print(type(start_dates))
    context = {
        "page_title": f"{year.get_spring_year()} B1G Schedule",
        "series": all_series,
        "start_dates": start_dates,
        "spring_year": spring_year,
    }
    template_path = "conference/conf_schedule.html"
    return shortcuts.render(request, template_path, context)


def week(request, spring_year, month, day):
    all_series = conf_models.ConfSeries.objects.filter(
        start_date=datetime.date(int(spring_year), int(month), int(day))    
    ).order_by("away_team__team_name")
    context = {
        "page_title": f"{year.get_spring_year()} B1G Schedule - {month}/{day}/{spring_year}",
        "series": all_series,
        "spring_year": spring_year,
    }
    template_path = "conference/conf_schedule_week.html"
    return shortcuts.render(request, template_path, context)
