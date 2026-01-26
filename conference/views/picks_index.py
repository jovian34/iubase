from django import shortcuts


def view(request, spring_year):
    template_path = "conference/picks_index.html"
    context = {
        "page_title": f"{spring_year} B1G Series Picks Home",
        "spring_year": spring_year,
    }
    return shortcuts.render(request, template_path, context)