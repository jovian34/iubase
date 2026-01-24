import datetime
from django import shortcuts, http, urls

from conference import forms as conf_forms
from conference import models as conf_models


spring_year = datetime.date.today().year
if datetime.date.today().month > 8:
    spring_year = spring_year + 1


def view(request, spring_year=spring_year):
    if not request.user.has_perm("conference.add_confseries"):
        return http.HttpResponseForbidden()
    elif request.method == "POST":
        form = conf_forms.AddConferenceSeriesForm(request.POST, spring_year=spring_year)
        if form.is_valid():
            conf_series = conf_models.ConfSeries(
                home_team=form.cleaned_data["home_team"],
                away_team=form.cleaned_data["away_team"],
                start_date=form.cleaned_data["start_date"],
            )
            conf_series.save()
        return shortcuts.redirect(urls.reverse("conf_schedule", args=[spring_year]))
    template_path = ("conference/add_series.html",)
    context = {
        "page_title": f"Add {spring_year} Conference Series",
        "form": conf_forms.AddConferenceSeriesForm(spring_year=spring_year),
        "spring_year": spring_year,
    }
    return shortcuts.render(request, template_path, context)
