from django import shortcuts
from conference import year


def view(request, spring_year):
    template_path = "conference/conf_schedule.html"
    context = {
        "page_title": f"{year.get_spring_year()} B1G Schedule"
    }
    return shortcuts.render(request, template_path, context)