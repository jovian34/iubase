from django import shortcuts, urls

from conference import models as conf_model


def away(request, conf_series):
    series = conf_model.ConfSeries.objects.get(pk=conf_series)
    if request.user.has_perm("conference.change_confseries"):
        series.away_wins = series.away_wins + 1
        series.save()
    template_path = "conference/conf_schedule.html#conf-series"
    context = {
        "series_pk": conf_series,
    }
    return shortcuts.render(request, template_path, context)


def home(request, conf_series):
    series = conf_model.ConfSeries.objects.get(pk=conf_series)
    if request.user.has_perm("conference.change_confseries"):
        series.home_wins = series.home_wins + 1
        series.save()
    return shortcuts.redirect(urls.reverse(
        "conf_schedule_week",
        kwargs = { 
            "spring_year": series.start_date.year,
            "month": series.start_date.month,
            "day": series.start_date.day,
        }
    ))


def tie(request, conf_series):
    series = conf_model.ConfSeries.objects.get(pk=conf_series)
    if request.user.has_perm("conference.change_confseries"):
        series.home_wins = float(series.home_wins) + 0.5
        series.away_wins = float(series.away_wins) + 0.5
        series.save()
    return shortcuts.redirect(urls.reverse(
        "conf_schedule_week",
        kwargs = { 
            "spring_year": series.start_date.year,
            "month": series.start_date.month,
            "day": series.start_date.day,
        }
    ))