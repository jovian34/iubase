from django import shortcuts


def view(request, conf, spring_year):
    return shortcuts.render(request, "conference/conf_year.html")