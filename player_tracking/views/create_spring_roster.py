from django import forms, http, shortcuts
from django.contrib.auth import decorators as auth
from django.db import transaction

from player_tracking import forms as pt_forms
from player_tracking.models import AnnualRoster


class SpringRosterEntryFormSet(forms.BaseFormSet):
    def __init__(self, *args, expected_roster_ids, **kwargs):
        self.expected_roster_ids = set(expected_roster_ids)
        super().__init__(*args, **kwargs)

    def clean(self):
        if any(self.errors):
            return

        submitted_roster_ids = [
            form.cleaned_data["fall_roster"] for form in self.forms
        ]
        if (
            len(submitted_roster_ids) != len(self.expected_roster_ids)
            or set(submitted_roster_ids) != self.expected_roster_ids
        ):
            raise forms.ValidationError(
                "The roster entries have changed. Reload the page and try again."
            )


@auth.login_required
def view(request, fall_year):
    if not request.user.has_perm("player_tracking.change_annualroster"):
        return http.HttpResponseForbidden()

    spring_year = int(fall_year) + 1
    players = (
        AnnualRoster.objects.filter(
            spring_year=spring_year,
            team__team_name="Indiana",
            status="Fall Roster",
        )
        .select_related("player")
        .order_by("jersey")
    )
    formset_class = forms.formset_factory(
        pt_forms.SpringRosterEntryForm,
        formset=SpringRosterEntryFormSet,
        extra=0,
    )
    initial = [
        {
            "fall_roster": roster.pk,
            "jersey": roster.jersey,
            "primary_position": roster.primary_position,
            "secondary_position": roster.secondary_position,
        }
        for roster in players
    ]
    expected_roster_ids = [roster["fall_roster"] for roster in initial]
    formset = formset_class(
        request.POST if request.method == "POST" else None,
        initial=initial,
        expected_roster_ids=expected_roster_ids,
    )
    if request.method == "POST" and formset.is_valid():
        save_spring_roster(formset, players)
        return shortcuts.redirect("pt_index")
    context = {
        "fall_year": int(fall_year),
        "spring_year": spring_year,
        "players": players,
        "formset": formset,
        "player_forms": zip(players, formset.forms),
    }
    return shortcuts.render(
        request,
        "player_tracking/create_spring_roster.html",
        context,
    )


@transaction.atomic
def save_spring_roster(formset, fall_rosters):
    fall_rosters_by_id = {roster.pk: roster for roster in fall_rosters}
    for form in formset:
        if not form.cleaned_data:
            continue
        roster = fall_rosters_by_id.get(form.cleaned_data["fall_roster"])
        if roster is None:
            continue
        if form.cleaned_data["include"]:
            roster.status = "Spring Roster"
            roster.jersey = form.cleaned_data["jersey"]
            roster.primary_position = form.cleaned_data["primary_position"]
            roster.secondary_position = form.cleaned_data["secondary_position"]
        else:
            roster.status = "Fall Roster"
        roster.save(
            update_fields=[
                "status",
                "jersey",
                "primary_position",
                "secondary_position",
            ]
        )
