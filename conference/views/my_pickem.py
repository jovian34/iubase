from django import shortcuts
from django.contrib.auth import decorators as auth


@auth.login_required
def view(request, spring_year):
    content = {
        "page_title": f"My {spring_year} Pick'em"
    }
    template_path = "conference/my_pickem.html"
    return shortcuts.render(request, template_path, content)