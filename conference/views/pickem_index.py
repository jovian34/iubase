from django import shortcuts


def view(request, spring_year):
    template_path = "conference/pickem_index.html"
    context = {
        "page_title": f"{spring_year} B1G Series Pick'em Home",
        "spring_year": spring_year,
    }
    return shortcuts.render(request, template_path, context)