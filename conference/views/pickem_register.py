from django import shortcuts
from django.contrib.auth import decorators as auth

from conference import forms as conf_forms
from conference import models as conf_models


@auth.login_required
def view(request, spring_year):
    if request.method == "POST":
        form = conf_forms.PickemRegistrationForm(request.POST)
        if form.is_valid():
            register = conf_models.PickemRegisterAnnual.objects.create(
                user=request.user,
                spring_year=spring_year,
                display_name=form.cleaned_data["display_name"],
                agree_to_terms=True,
                make_public=form.cleaned_data["make_public"]
            )
            register.save()
        
    form = conf_forms.PickemRegistrationForm()
    template_path = "conference/pickem_register.html"
    context = {
        "page_title": "Register for iubase.com B1G Pick'em",
        "spring_year": spring_year,
        "form": form,
    }
    return shortcuts.render(request, template_path, context)