from django import shortcuts


def view(request, series, pick):
    template_path = "conference/my_pickem.html#series"
    context = {

    }
    return shortcuts.render(request, template_path, context)