from django import shortcuts, urls
from django.contrib.auth import decorators as auth

from conference import models as conf_models


@auth.login_required
def view(request, spring_year):
    registration = conf_models.PickemRegisterAnnual.objects.filter(
        user=request.user,
        spring_year=spring_year,
    )
    if not registration.exists():
        return shortcuts.redirect(urls.reverse("pickem_register", args=[spring_year]))

    content = {
        "page_title": f"My {spring_year} Pick'em"
    }
    template_path = "conference/my_pickem.html"
    return shortcuts.render(request, template_path, content)