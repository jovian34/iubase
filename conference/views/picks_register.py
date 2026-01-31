from django import shortcuts
from django.contrib.auth import decorators as auth


@auth.login_required
def view(request):
    template_path = "conference/picks_register.html"
    context = {
        "page_title": "Register for iubase.com B1G Picks",
    }
    return shortcuts.render(request, template_path, context)