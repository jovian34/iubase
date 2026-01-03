from django import shortcuts

def view(request, spring_year):
    template_path = "conference/standings.html"
    context = {

    }
    return shortcuts.render(request, template_path, context)