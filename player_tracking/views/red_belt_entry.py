from django import shortcuts
from django.contrib.auth import decorators as auth
from django.http import Http404
from django.utils import timezone

from player_tracking import forms
from player_tracking.logic import red_belts


@auth.login_required
def view(request, spring_year):
    red_belts.require_add_accolade_permission(request)
    spring_year = int(spring_year)
    if spring_year > timezone.localdate().year:
        raise Http404

    form = forms.RedBeltEntryForm(
        request.POST or None,
        spring_year=spring_year,
    )
    if request.method == "POST" and form.is_valid():
        red_belts.save_weekly_red_belts(form)
        return shortcuts.redirect("red_belt_entry", spring_year=spring_year)

    context = {
        "form": form,
        "page_title": f"Weekly Red Belt Entry for {spring_year}",
        "spring_year": spring_year,
        "years": red_belts.get_spring_roster_years(),
    }
    if request.META.get("HTTP_HX_REQUEST"):
        template_path = "player_tracking/partials/red_belt_entry_form.html"
    else:
        template_path = "player_tracking/red_belt_entry.html"
    return shortcuts.render(request, template_path, context)


@auth.login_required
def redirect_to_current_year(request):
    red_belts.require_add_accolade_permission(request)
    return shortcuts.redirect("red_belt_entry", spring_year=timezone.localdate().year)
