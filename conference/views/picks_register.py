from django import shortcuts


def view(request):
    template_path = "conference/picks_register.html"
    context = {
        "page_title": "Register for iubase.com B1G Picks",
    }
    return shortcuts.render(request, template_path, context)