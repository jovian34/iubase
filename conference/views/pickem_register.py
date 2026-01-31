from django import shortcuts
from django.contrib.auth import decorators as auth


@auth.login_required
def view(request):
    template_path = "conference/pickem_register.html"
    context = {
        "page_title": "Register for iubase.com B1G Pick'em",
    }
    return shortcuts.render(request, template_path, context)