import pytest
from bs4 import BeautifulSoup
from django.urls import reverse
from datetime import date

from accounts.tests.fixtures import logged_user_schwarbs
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.models import AnnualRoster
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.accolades import accolades
from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)

this_year = date.today().year
spring_roster_form_path = f"/player_tracking/create_spring_roster/{this_year}/"


@pytest.mark.django_db
def test_fall_roster_renders(client, players, teams, annual_rosters):
    response = client.get(
        reverse("fall_roster", args=[f"{this_year - 1}"]),
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert "Total Roster Length: 6" in response.content.decode()
    assert f"Fall {this_year - 1} Roster" in response.content.decode()
    assert "Nathan Ball" in response.content.decode()
    assert "Nick Mitchell" in response.content.decode()
    assert "Jack Moffitt" in response.content.decode()
    assert "Brayden" not in response.content.decode()


@pytest.mark.django_db
def test_fall_roster_shows_spring_roster_link_to_roster_editor(
    admin_client, players, teams, annual_rosters
):
    AnnualRoster.objects.create(
        spring_year=this_year + 1,
        status="Fall Roster",
        player=players.jake_stadler,
        team=teams.indiana,
        jersey=9,
        primary_position="Catcher",
        secondary_position="First Base",
    )

    response = admin_client.get(
        reverse("fall_roster", args=[this_year]),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert f"Create Spring {this_year + 1} Roster" in response.content.decode()
    assert f'href="{spring_roster_form_path}"' in response.content.decode()


@pytest.mark.django_db
def test_fall_roster_hides_spring_roster_link_without_change_permission(
    client, logged_user_schwarbs, players, teams, annual_rosters
):
    AnnualRoster.objects.create(
        spring_year=this_year + 1,
        status="Fall Roster",
        player=players.jake_stadler,
        team=teams.indiana,
        jersey=9,
        primary_position="Catcher",
    )

    response = client.get(
        reverse("fall_roster", args=[this_year]),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert f"Create Spring {this_year + 1} Roster" not in response.content.decode()


@pytest.mark.django_db
def test_create_spring_roster_form_lists_fall_roster_players(
    admin_client, players, teams, annual_rosters
):
    AnnualRoster.objects.create(
        spring_year=this_year + 1,
        status="Fall Roster",
        player=players.jake_stadler,
        team=teams.indiana,
        jersey=9,
        primary_position="Catcher",
        secondary_position="First Base",
    )

    response = admin_client.get(spring_roster_form_path)
    page = BeautifulSoup(response.content, "html.parser")

    assert response.status_code == 200
    assert page.find(string="Jake Stadler")
    player_link = page.find(
        "a", href=reverse("single_player_page", args=[players.jake_stadler.pk])
    )
    assert player_link.get("target") == "_blank"
    include_checkbox = page.find("input", {"name": "form-0-include"})
    assert include_checkbox.has_attr("checked")
    assert page.find("input", {"name": "form-0-jersey"})["value"] == "9"
    assert page.find("select", {"name": "form-0-primary_position"}).find(
        "option", selected=True
    )["value"] == "Catcher"
    assert page.find("select", {"name": "form-0-secondary_position"}).find(
        "option", selected=True
    )["value"] == "First Base"


@pytest.mark.django_db
def test_create_spring_roster_form_hides_players_already_on_spring_roster(
    admin_client, players, teams
):
    AnnualRoster.objects.create(
        spring_year=this_year + 1,
        status="Spring Roster",
        player=players.jake_stadler,
        team=teams.indiana,
        jersey=9,
        primary_position="Catcher",
    )
    AnnualRoster.objects.create(
        spring_year=this_year + 1,
        status="Fall Roster",
        player=players.ryan_kraft,
        team=teams.indiana,
        jersey=29,
        primary_position="Pitcher",
    )

    response = admin_client.get(spring_roster_form_path)
    page = BeautifulSoup(response.content, "html.parser")

    assert response.status_code == 200
    assert page.find(string="Jake Stadler") is None
    assert page.find(string="Ryan Kraft")


@pytest.mark.django_db
def test_create_spring_roster_form_forbidden_without_change_permission(
    client, logged_user_schwarbs
):
    response = client.get(spring_roster_form_path)

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_spring_roster_submission_promotes_checked_players_and_keeps_others_in_fall(
    admin_client, players, teams, annual_rosters
):
    moving_player = AnnualRoster.objects.create(
        spring_year=this_year + 1,
        status="Fall Roster",
        player=players.jake_stadler,
        team=teams.indiana,
        jersey=9,
        primary_position="Catcher",
        secondary_position="First Base",
    )
    non_moving_player = AnnualRoster.objects.create(
        spring_year=this_year + 1,
        status="Fall Roster",
        player=players.ryan_kraft,
        team=teams.indiana,
        jersey=29,
        primary_position="Pitcher",
    )
    response = admin_client.post(
        spring_roster_form_path,
        {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "2",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
            "form-0-fall_roster": str(moving_player.pk),
            "form-0-include": "on",
            "form-0-jersey": "10",
            "form-0-primary_position": "Catcher",
            "form-0-secondary_position": "Designated Hitter",
            "form-1-fall_roster": str(non_moving_player.pk),
            "form-1-jersey": "29",
            "form-1-primary_position": "Pitcher",
            "form-1-secondary_position": "",
        },
    )

    assert response.status_code == 302
    assert response["Location"] == reverse("pt_index")
    moving_player.refresh_from_db()
    non_moving_player.refresh_from_db()
    assert moving_player.status == "Spring Roster"
    assert moving_player.jersey == 10
    assert moving_player.primary_position == "Catcher"
    assert moving_player.secondary_position == "Designated Hitter"
    assert non_moving_player.status == "Fall Roster"
    assert AnnualRoster.objects.filter(
        player=players.jake_stadler,
        spring_year=this_year + 1,
    ).count() == 1


@pytest.mark.django_db
def test_invalid_spring_roster_submission_does_not_save_any_player(
    admin_client, players, teams
):
    moving_player = AnnualRoster.objects.create(
        spring_year=this_year + 1,
        status="Fall Roster",
        player=players.jake_stadler,
        team=teams.indiana,
        jersey=9,
        primary_position="Catcher",
        secondary_position="First Base",
    )
    other_player = AnnualRoster.objects.create(
        spring_year=this_year + 1,
        status="Fall Roster",
        player=players.ryan_kraft,
        team=teams.indiana,
        jersey=29,
        primary_position="Pitcher",
    )

    response = admin_client.post(
        spring_roster_form_path,
        {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "2",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
            "form-0-fall_roster": str(moving_player.pk),
            "form-0-include": "on",
            "form-0-jersey": "10",
            "form-0-primary_position": "Not a position",
            "form-0-secondary_position": "Designated Hitter",
            "form-1-fall_roster": str(other_player.pk),
            "form-1-include": "on",
            "form-1-jersey": "30",
            "form-1-primary_position": "Catcher",
            "form-1-secondary_position": "",
        },
    )

    assert response.status_code == 200
    assert "Select a valid choice." in response.content.decode()
    moving_player.refresh_from_db()
    other_player.refresh_from_db()
    assert moving_player.status == "Fall Roster"
    assert moving_player.jersey == 9
    assert moving_player.primary_position == "Catcher"
    assert moving_player.secondary_position == "First Base"
    assert other_player.status == "Fall Roster"
    assert other_player.jersey == 29
    assert other_player.primary_position == "Pitcher"


@pytest.mark.django_db
def test_spring_roster_submission_with_unknown_roster_id_saves_no_players(
    admin_client, players, teams
):
    first_player = AnnualRoster.objects.create(
        spring_year=this_year + 1,
        status="Fall Roster",
        player=players.jake_stadler,
        team=teams.indiana,
        jersey=9,
        primary_position="Catcher",
    )
    second_player = AnnualRoster.objects.create(
        spring_year=this_year + 1,
        status="Fall Roster",
        player=players.ryan_kraft,
        team=teams.indiana,
        jersey=29,
        primary_position="Pitcher",
    )

    response = admin_client.post(
        spring_roster_form_path,
        {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "2",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
            "form-0-fall_roster": "999999999",
            "form-0-include": "on",
            "form-0-jersey": "10",
            "form-0-primary_position": "Catcher",
            "form-0-secondary_position": "",
            "form-1-fall_roster": str(second_player.pk),
            "form-1-include": "on",
            "form-1-jersey": "30",
            "form-1-primary_position": "Catcher",
            "form-1-secondary_position": "",
        },
    )

    assert response.status_code == 200
    first_player.refresh_from_db()
    second_player.refresh_from_db()
    assert first_player.status == "Fall Roster"
    assert first_player.jersey == 9
    assert second_player.status == "Fall Roster"
    assert second_player.jersey == 29
    assert second_player.primary_position == "Pitcher"


@pytest.mark.django_db
def test_fall_roster_renders_player_height_and_weight(
    client, players, teams, annual_rosters
):
    players.ryan_kraft.height = 75
    players.ryan_kraft.weight = 200
    players.ryan_kraft.save()

    response = client.get(
        reverse("fall_roster", args=[f"{this_year - 1}"]),
        HTTP_HX_REQUEST="true",
    )

    output = response.content.decode()
    assert "Height: 6 ft. 3 inches" in output
    assert "Weight: 200 lbs." in output


@pytest.mark.django_db
def test_fall_roster_shows_percentage_from_outside_indiana(
    client, players, teams, annual_rosters
):
    players.jake_stadler.home_state = "IN"
    players.jake_stadler.save()
    players.ryan_kraft.home_state = "OH"
    players.ryan_kraft.save()

    response = client.get(
        reverse("fall_roster", args=[f"{this_year - 1}"]),
        HTTP_HX_REQUEST="true",
    )

    assert "50% are from outside of Indiana" in response.content.decode()


@pytest.mark.django_db
def test_fall_roster_renders_full_page_without_HTMX_call(
    client, players, teams, annual_rosters
):
    response = client.get(
        reverse("fall_roster", args=[f"{this_year - 1}"]),
    )
    assert response.status_code == 302
    response = client.get(
        reverse("fall_roster", args=[f"{this_year - 1}"]),
        follow=True,
    )
    assert response.status_code == 200
    assert "<title>Players for Fall Seasons by Year</title>" in response.content.decode()
    assert (
        f'hx-get="/player_tracking/fall_players_redirect/{this_year - 1}/" hx-trigger="load"'
        in response.content.decode()
    )


@pytest.mark.django_db
def test_spring_roster_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("spring_roster", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert "Total Roster Length: 3" in response.content.decode()
    assert f"Spring {this_year - 1} Roster" in response.content.decode()
    assert "Nick Mitchell" not in response.content.decode()
    assert "Devin Taylor" in response.content.decode()


@pytest.mark.django_db
def test_spring_roster_renders_player_height_and_weight(
    client, players, teams, annual_rosters
):
    players.ryan_kraft.height = 75
    players.ryan_kraft.weight = 200
    players.ryan_kraft.save()

    response = client.get(reverse("spring_roster", args=[f"{this_year - 1}"]))

    output = response.content.decode()
    assert "Height: 6 ft. 3 inches" in output
    assert "Weight: 200 lbs." in output


@pytest.mark.django_db
def test_spring_roster_shows_percentage_from_outside_indiana(
    client, players, teams, annual_rosters
):
    players.ryan_kraft.home_state = "IN"
    players.ryan_kraft.save()
    players.devin_taylor.home_state = "OH"
    players.devin_taylor.save()

    response = client.get(reverse("spring_roster", args=[f"{this_year - 1}"]))

    assert "50% are from outside of Indiana" in response.content.decode()


@pytest.mark.django_db
def test_spring_roster_renders_accolade(
    client, players, teams, annual_rosters, accolades
):
    response = client.get(reverse("spring_roster", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert "B1G All-Conference Freshman Team" in response.content.decode()


@pytest.mark.django_db
def test_spring_roster_future_shows_not_aanounced(
    client, players, teams, annual_rosters
):
    response = client.get(reverse("spring_roster", args=[f"{this_year + 1}"]))
    assert response.status_code == 200
    assert "Roster not fully announced" in response.content.decode()
