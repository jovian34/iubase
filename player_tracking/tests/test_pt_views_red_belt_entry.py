from datetime import date

import pytest
from django.urls import reverse

from accounts.tests.fixtures import logged_user_schwarbs
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.models import Accolade, AnnualRoster
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players


this_year = date.today().year


@pytest.mark.django_db
def test_red_belt_entry_page_renders(admin_client):
    response = admin_client.get(reverse("red_belt_entry", args=[this_year]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_red_belt_entry_page_redirects_not_logged_in(client):
    response = client.get(reverse("red_belt_entry", args=[this_year]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_red_belt_entry_page_asks_for_password_not_logged_in(client):
    response = client.get(
        reverse("red_belt_entry", args=[this_year]),
        follow=True,
    )
    assert response.status_code == 200
    assert "Sign In Via Google" in response.content.decode()


@pytest.mark.django_db
def test_red_belt_entry_page_forbidden_without_add_accolade_permission(
    client, logged_user_schwarbs
):
    response = client.get(reverse("red_belt_entry", args=[this_year]))
    assert response.status_code == 403
    assert "Forbidden Error Recorded" in response.content.decode()


@pytest.mark.django_db
def test_red_belt_entry_without_year_redirects_to_current_year(admin_client):
    response = admin_client.get("/player_tracking/red_belt_entry/")
    assert response.status_code == 302
    assert response.url == reverse("red_belt_entry", args=[this_year])


@pytest.mark.django_db
def test_red_belt_entry_future_year_returns_not_found(admin_client):
    response = admin_client.get(reverse("red_belt_entry", args=[this_year + 1]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_red_belt_entry_renders_full_page_and_form_for_normal_request(
    admin_client, annual_rosters
):
    response = admin_client.get(reverse("red_belt_entry", args=[this_year - 1]))
    rendered_templates = [template.name for template in response.templates]
    assert "player_tracking/red_belt_entry.html" in rendered_templates
    assert "player_tracking/partials/red_belt_entry_form.html" in rendered_templates
    assert f"Weekly Red Belt Entry for {this_year - 1}" in response.content.decode()


@pytest.mark.django_db
def test_red_belt_entry_renders_only_form_partial_for_htmx_request(
    admin_client, annual_rosters
):
    response = admin_client.get(
        reverse("red_belt_entry", args=[this_year - 1]),
        HTTP_HX_REQUEST="true",
    )
    rendered_templates = [template.name for template in response.templates]
    assert response.status_code == 200
    assert "player_tracking/partials/red_belt_entry_form.html" in rendered_templates
    assert "player_tracking/red_belt_entry.html" not in rendered_templates


@pytest.mark.django_db
def test_red_belt_entry_shows_only_existing_non_future_indiana_spring_years(
    admin_client, annual_rosters, players, teams
):
    AnnualRoster.objects.create(
        spring_year=this_year + 1,
        status="Spring Roster",
        player=players.peter_dubie,
        team=teams.indiana,
        primary_position="Pitcher",
    )
    response = admin_client.get(reverse("red_belt_entry", args=[this_year]))
    output = response.content.decode()
    assert f">{this_year}</button>" in output
    assert f">{this_year - 1}</button>" in output
    assert f">{this_year + 1}</button>" not in output
    assert f">{this_year - 2}</button>" not in output


@pytest.mark.django_db
def test_red_belt_entry_year_buttons_use_htmx_and_update_browser_url(
    admin_client, annual_rosters
):
    response = admin_client.get(reverse("red_belt_entry", args=[this_year]))
    output = response.content.decode()
    previous_year_url = reverse("red_belt_entry", args=[this_year - 1])
    assert f'hx-get="{previous_year_url}"' in output
    assert 'hx-target="#red-belt-entry-form"' in output
    assert 'hx-push-url="true"' in output


@pytest.mark.django_db
def test_red_belt_entry_form_has_date_and_three_fixed_award_fields(
    admin_client, annual_rosters
):
    response = admin_client.get(reverse("red_belt_entry", args=[this_year - 1]))
    form = response.context["form"]
    assert set(form.fields) == {"award_date", "pitcher", "hitter", "defender"}
    assert "Joey DeNato Weekly Red Belt for pitching" in response.content.decode()
    assert "Alex Dickerson Weekly Red Belt for hitting" in response.content.decode()
    assert "Tony Butler Weekly Red Belt for defense" in response.content.decode()


@pytest.mark.django_db
def test_red_belt_hitting_and_defense_choices_are_indiana_spring_roster_only(
    admin_client, annual_rosters
):
    response = admin_client.get(reverse("red_belt_entry", args=[this_year]))
    form = response.context["form"]
    hitting_choices = form.fields["hitter"].queryset
    defense_choices = form.fields["defender"].queryset
    assert annual_rosters.rk_jr in hitting_choices
    assert annual_rosters.dt_soph in hitting_choices
    assert annual_rosters.rk_jr in defense_choices
    assert annual_rosters.dt_soph in defense_choices
    assert annual_rosters.js_jr not in hitting_choices
    assert annual_rosters.nb_fresh not in hitting_choices
    assert annual_rosters.hc_soph not in hitting_choices
    assert annual_rosters.dt_fresh not in hitting_choices


@pytest.mark.django_db
def test_red_belt_pitching_choices_include_primary_pitchers_only_from_roster(
    admin_client, annual_rosters
):
    response = admin_client.get(reverse("red_belt_entry", args=[this_year - 1]))
    pitching_choices = response.context["form"].fields["pitcher"].queryset
    assert annual_rosters.rk_soph in pitching_choices
    assert annual_rosters.br_fresh in pitching_choices
    assert annual_rosters.dt_fresh not in pitching_choices
    assert annual_rosters.hc_fresh not in pitching_choices
    assert annual_rosters.rk_jr not in pitching_choices


@pytest.mark.django_db
def test_red_belt_pitching_choices_include_secondary_pitchers(
    admin_client, annual_rosters
):
    annual_rosters.dt_fresh.secondary_position = "Pitcher"
    annual_rosters.dt_fresh.save()
    response = admin_client.get(reverse("red_belt_entry", args=[this_year - 1]))
    pitching_choices = response.context["form"].fields["pitcher"].queryset
    assert annual_rosters.dt_fresh in pitching_choices


@pytest.mark.django_db
def test_red_belt_entry_rejects_award_date_from_another_year(
    admin_client, annual_rosters
):
    response = admin_client.post(
        reverse("red_belt_entry", args=[this_year - 1]),
        {
            "award_date": date(this_year, 3, 1),
            "pitcher": annual_rosters.rk_soph.pk,
            "hitter": annual_rosters.dt_fresh.pk,
            "defender": annual_rosters.br_fresh.pk,
        },
    )
    assert response.status_code == 200
    assert response.context["form"].errors.get("award_date")
    assert not Accolade.objects.exists()


@pytest.mark.django_db
def test_red_belt_entry_rejects_player_outside_field_choices(
    admin_client, annual_rosters
):
    response = admin_client.post(
        reverse("red_belt_entry", args=[this_year - 1]),
        {
            "award_date": date(this_year - 1, 3, 1),
            "pitcher": annual_rosters.dt_fresh.pk,
            "hitter": annual_rosters.hc_fresh.pk,
            "defender": annual_rosters.rk_jr.pk,
        },
    )
    form = response.context["form"]
    assert form.errors.get("pitcher")
    assert form.errors.get("hitter")
    assert form.errors.get("defender")
    assert not Accolade.objects.exists()


@pytest.mark.django_db
def test_red_belt_entry_creates_three_fixed_accolades(
    admin_client, annual_rosters
):
    award_date = date(this_year - 1, 3, 1)
    admin_client.post(
        reverse("red_belt_entry", args=[this_year - 1]),
        {
            "award_date": award_date,
            "pitcher": annual_rosters.rk_soph.pk,
            "hitter": annual_rosters.dt_fresh.pk,
            "defender": annual_rosters.br_fresh.pk,
        },
    )
    red_belts = Accolade.objects.filter(award_date=award_date)
    assert red_belts.count() == 3
    assert red_belts.get(
        name="Joey DeNato Weekly Red Belt for pitching",
        player=annual_rosters.rk_soph.player,
        annual_roster=annual_rosters.rk_soph,
    )
    assert red_belts.get(
        name="Alex Dickerson Weekly Red Belt for hitting",
        player=annual_rosters.dt_fresh.player,
        annual_roster=annual_rosters.dt_fresh,
    )
    assert red_belts.get(
        name="Tony Butler Weekly Red Belt for defense",
        player=annual_rosters.br_fresh.player,
        annual_roster=annual_rosters.br_fresh,
    )
