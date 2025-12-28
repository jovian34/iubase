from django import shortcuts


def view(request):
    template_path = "conference/add_series.html",
    context = {

    }
    return shortcuts.render(request, template_path, context)