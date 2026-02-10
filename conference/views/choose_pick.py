from django import shortcuts

from conference import models as conf_models


def home(request, series):
    conf_series = conf_models.ConfSeries.objects.get(pk=series)
    registration = conf_models.PickemRegisterAnnual.objects.get(
        user=request.user,
        spring_year=conf_series.start_date.year,
    )
    new_pick = conf_models.Pick.objects.create(
        user=registration,
        series=conf_series,
        pick_home=True,
    )
    new_pick.save()
    pick = conf_models.Pick.objects.get(
        user=registration,
        series=conf_series,
    )
    template_path = "conference/partials/picked_series.html"
    context = {
        "matchup": conf_series,
        "pick": pick,
    }
    return shortcuts.render(request, template_path, context)


def away(request, series):
    conf_series = conf_models.ConfSeries.objects.get(pk=series)
    registration = conf_models.PickemRegisterAnnual.objects.get(
        user=request.user,
        spring_year=conf_series.start_date.year,
    )
    new_pick = conf_models.Pick.objects.create(
        user=registration,
        series=conf_series,
        pick_home=False,
    )
    template_path = "conference/partials/picked_series.html"
    context = {
        "matchup": conf_series,
    }
    return shortcuts.render(request, template_path, context)