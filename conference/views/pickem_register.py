from django import shortcuts
from django.contrib.auth import decorators as auth

from conference import forms as conf_forms


@auth.login_required
def view(request, spring_year):
    if request.method == "POST":
        form = conf_forms.PickemRegistrationForm(request.POST)
        
    form = conf_forms.PickemRegistrationForm()
    template_path = "conference/pickem_register.html"
    context = {
        "page_title": "Register for iubase.com B1G Pick'em",
        "spring_year": spring_year,
        "form": form,
    }
    return shortcuts.render(request, template_path, context)