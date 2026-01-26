from django import shortcuts
import datetime

from conference.logic import year


def view(request):
    template_path = "conference/conf_index.html"
    context = {
        "page_title": "B1G Conference Apps",
        "spring_year": year.get_spring_year(),
        "this_year": datetime.date.today().year,
    }
    return shortcuts.render(request, template_path, context)