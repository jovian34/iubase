import datetime
from django import shortcuts, http

from conference import forms as conf_forms


spring_year = datetime.date.today().year
if datetime.date.today().month > 8:
    spring_year = spring_year + 1


def view(request, spring_year=spring_year):
    if not request.user.has_perm("conference.add_confseries"):
        return http.HttpResponseForbidden()
    
    template_path = "conference/add_series.html",
    context = {
        "page_title": f"Add {spring_year} Conference Series",
        "form": conf_forms.AddConferenceSeriesForm(spring_year=spring_year),
        "spring_year": spring_year,
    }
    return shortcuts.render(request, template_path, context)