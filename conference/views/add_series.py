import datetime

from django import shortcuts

spring_year = datetime.date.today().year
if datetime.date.today().month > 8:
    spring_year = spring_year + 1


def view(request, spring_year=spring_year):
    template_path = "conference/add_series.html",
    context = {

    }
    return shortcuts.render(request, template_path, context)