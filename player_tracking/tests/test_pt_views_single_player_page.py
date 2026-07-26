import pytest
from bs4 import BeautifulSoup
from django.contrib.auth.models import Permission
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)
from player_tracking.tests.fixtures.accolades import accolades
from live_game_blog.tests.fixtures.teams import teams
from accounts.tests.fixtures import logged_user_schwarbs


this_year = date.today().year

PLAYER_CHANGE_BUTTON_PERMISSIONS = (
    ("change_player", "edit player info"),
    ("add_annualroster", "add roster year"),
    ("add_transaction", "add transaction"),
    ("add_summerassign", "add summer assignment"),
    ("add_accolade", "add accolade"),
)

PLAYER_PAGE_SECTION_CONTROLS = (
    ("player-info", "edit player info", "edit-player-info-control"),
    ("annual-rosters", "add roster year", "add-roster-year-control"),
    ("transactions", "add transaction", "add-transaction-control"),
    ("summer-ball", "add summer assignment", "add-summer-assignment-control"),
    ("other-accolades", "add accolade", "add-accolade-control"),
)

PLAYER_CHANGE_FORM_TARGETS = (
    ("edit_player", "player-info"),
    ("add_roster_year", "annual-rosters"),
    ("add_transaction", "transactions"),
    ("add_summer_assignment", "summer-ball"),
    ("add_accolade", "other-accolades"),
)


def grant_player_tracking_permission(user, permission_codename):
    permission = Permission.objects.get(
        content_type__app_label="player_tracking",
        codename=permission_codename,
    )
    user.user_permissions.add(permission)


def parse_response(response):
    return BeautifulSoup(response.content, "html.parser")


@pytest.mark.django_db
def test_single_player_page_renders_one_player_only(client, players, annual_rosters):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in response.content.decode()
    assert "Nick" not in response.content.decode()


@pytest.mark.django_db
def test_single_player_page_raises_404_if_not_in_database(
    client, players, annual_rosters
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[5748454752],
        )
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_single_player_page_renders_summer_teams(
    client, players, annual_rosters, summer_assign, summer_leagues, summer_teams
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in response.content.decode()
    assert "Summer Ball:" in response.content.decode()
    assert (
        f"{this_year}: USA Collegiate National Team of the International Friendship League"
        in response.content.decode()
    )


@pytest.mark.django_db
def test_single_player_page_renders_transfer_player_old_team(
    client, annual_rosters, players
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.nick_mitchell.pk],
        )
    )
    assert response.status_code == 200
    assert "Nick Mitchell" in response.content.decode()
    assert "Devin" not in response.content.decode()
    assert "Miami (Ohio)" in response.content.decode()


@pytest.mark.django_db
def test_single_player_page_renders_action_shot_for_that_player(
    client, players, annual_rosters
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert "https://live.staticflickr.com/65535/54014518896_5c58571da6_o.jpg" in str(
        response.content
    )
    assert (
        "https://iubase.com/wp-content/uploads/2024/11/53704071552_13227a46a0_k.jpg"
        not in response.content.decode()
    )


@pytest.mark.django_db
def test_single_player_page_renders_player_handedness_height_and_weight(
    client,
    players,
    annual_rosters,
):
    player = players.devin_taylor
    player.bats = "Left"
    player.throws = "Right"
    player.height = 74
    player.weight = 215
    player.save(update_fields=["bats", "throws", "height", "weight"])

    response = client.get(reverse("single_player_page", args=[player.pk]))
    player_details = parse_response(response).find(id="player-details")
    assert player_details is not None
    details_text = player_details.get_text(" ", strip=True)

    assert "Bats: Left" in details_text
    assert "Throws: Right" in details_text
    assert "Height: 6 ft. 2 inches" in details_text
    assert "Weight: 215 lbs." in details_text


@pytest.mark.django_db
def test_single_player_page_renders_hometown_and_high_school_without_usa(
    client,
    players,
    annual_rosters,
):
    player = players.devin_taylor
    player.home_city = "Cincinnati"
    player.home_state = "OH"
    player.home_country = "USA"
    player.high_school = "La Salle High School"
    player.save(
        update_fields=["home_city", "home_state", "home_country", "high_school"]
    )

    response = client.get(reverse("single_player_page", args=[player.pk]))
    player_details = parse_response(response).find(id="player-details")
    assert player_details is not None
    details_text = player_details.get_text(" ", strip=True)

    assert "Hometown: Cincinnati, OH" in details_text
    assert "USA" not in details_text
    assert "High School: La Salle High School" in details_text


@pytest.mark.django_db
def test_single_player_page_includes_country_for_international_hometown(
    client,
    players,
    annual_rosters,
):
    player = players.devin_taylor
    player.home_city = "Toronto"
    player.home_state = "ON"
    player.home_country = "Canada"
    player.save(update_fields=["home_city", "home_state", "home_country"])

    response = client.get(reverse("single_player_page", args=[player.pk]))
    player_details = parse_response(response).find(id="player-details")
    assert player_details is not None
    details_text = player_details.get_text(" ", strip=True)

    assert "Hometown: Toronto, ON, Canada" in details_text


@pytest.mark.django_db
def test_single_player_page_renders_player_details_below_photos(
    client,
    players,
    annual_rosters,
):
    player = players.devin_taylor
    player.height = 74
    player.weight = 215
    player.save(update_fields=["height", "weight"])

    response = client.get(reverse("single_player_page", args=[player.pk]))
    player_info = parse_response(response).find(id="player-info")
    player_info_elements = list(player_info.descendants)
    headshot = player_info.find("img", class_="headshot")
    player_details = player_info.find(id="player-details")
    edit_control = player_info.find(id="edit-player-info-control")

    assert headshot is not None
    assert player_details is not None
    assert edit_control is not None
    assert player_info_elements.index(headshot) < player_info_elements.index(
        player_details
    )
    assert player_info_elements.index(player_details) < player_info_elements.index(
        edit_control
    )


@pytest.mark.django_db
def test_single_player_page_renders_generic_action_shot_if_one_does_not_exist(
    client, players, annual_rosters
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.brayden_risedorph.pk],
        )
    )
    assert (
        "https://iubase.com/wp-content/uploads/2024/11/53704071552_13227a46a0_k.jpg"
        in response.content.decode()
    )


@pytest.mark.django_db
def test_single_player_page_renders_accolade_org_and_name(
    client, players, annual_rosters, accolades
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in response.content.decode()


@pytest.mark.django_db
def test_single_player_page_omits_add_and_edit_buttons_not_logged_in(
    client, players, annual_rosters
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in response.content.decode()
    assert "add accolade</button>" not in response.content.decode()
    assert "add summer assignment</button>" not in response.content.decode()
    assert "add transaction</button>" not in response.content.decode()
    assert "add roster year</button>"not  in response.content.decode()
    assert "edit player info</button>" not in response.content.decode()
    assert "B1G First Team All-Conference Outfielder" not in response.content.decode()


@pytest.mark.django_db
def test_single_player_page_omits_add_and_edit_buttons_without_perms(
    client, players, annual_rosters, logged_user_schwarbs
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in response.content.decode()
    assert "add accolade</button>" not in response.content.decode()
    assert "add summer assignment</button>" not in response.content.decode()
    assert "add transaction</button>" not in response.content.decode()
    assert "add roster year</button>"not  in response.content.decode()
    assert "edit player info</button>" not in response.content.decode()
    assert "B1G First Team All-Conference Outfielder" not in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("permission_codename", "permitted_button"),
    PLAYER_CHANGE_BUTTON_PERMISSIONS,
)
def test_single_player_page_renders_only_button_allowed_by_permission(
    client,
    players,
    annual_rosters,
    logged_user_schwarbs,
    permission_codename,
    permitted_button,
):
    grant_player_tracking_permission(logged_user_schwarbs, permission_codename)

    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )

    assert response.status_code == 200
    output = response.content.decode()
    assert f"{permitted_button}</button>" in output
    for _, other_button in PLAYER_CHANGE_BUTTON_PERMISSIONS:
        if other_button != permitted_button:
            assert f"{other_button}</button>" not in output


@pytest.mark.django_db
def test_player_change_controls_render_in_separate_page_sections(
    admin_client,
    players,
    annual_rosters,
):
    response = admin_client.get(
        reverse("single_player_page", args=[players.devin_taylor.pk])
    )
    page = parse_response(response)

    for section_id, button_text, control_id in PLAYER_PAGE_SECTION_CONTROLS:
        section = page.find(id=section_id)
        assert section is not None
        control = section.find(id=control_id)
        assert control is not None
        button = control.find("button", string=button_text)
        assert button is not None
        assert button["hx-target"] == f"#{control_id}"


@pytest.mark.django_db
def test_edit_player_control_renders_before_annual_rosters(
    admin_client,
    players,
    annual_rosters,
):
    response = admin_client.get(
        reverse("single_player_page", args=[players.devin_taylor.pk])
    )
    page = parse_response(response)

    player_info = page.find(id="player-info")
    annual_rosters_section = page.find(id="annual-rosters")
    assert player_info is not None
    assert annual_rosters_section is not None
    assert player_info.find("button", string="edit player info")
    assert list(page.descendants).index(player_info) < list(page.descendants).index(
        annual_rosters_section
    )


@pytest.mark.django_db
def test_add_accolade_control_renders_above_most_recent_roster(
    admin_client,
    players,
    annual_rosters,
):
    response = admin_client.get(
        reverse("single_player_page", args=[players.devin_taylor.pk])
    )
    page = parse_response(response)
    annual_rosters_section = page.find(id="annual-rosters")

    accolade_control = annual_rosters_section.find(id="add-roster-accolade-control")
    assert accolade_control is not None
    add_accolade_button = accolade_control.find("button", string="add accolade")
    assert add_accolade_button is not None
    assert add_accolade_button["hx-get"] == reverse(
        "add_accolade",
        args=[players.devin_taylor.pk],
    )
    assert add_accolade_button["hx-target"] == "#add-roster-accolade-control"

    most_recent_roster = annual_rosters_section.find("h2")
    section_elements = list(annual_rosters_section.descendants)
    assert section_elements.index(accolade_control) < section_elements.index(
        most_recent_roster
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("view_name", "section_id"),
    PLAYER_CHANGE_FORM_TARGETS,
)
def test_player_change_forms_submit_with_htmx_to_their_page_section(
    admin_client,
    players,
    annual_rosters,
    summer_assign,
    view_name,
    section_id,
):
    form_url = reverse(view_name, args=[players.devin_taylor.pk])
    response = admin_client.get(form_url, HTTP_HX_REQUEST="true")
    form = parse_response(response).find("form")

    assert form["hx-post"] == form_url
    assert form["hx-target"] == f"#{section_id}"


@pytest.mark.django_db
def test_single_player_page_renders_accolades_in_reverse_date_order(
    client, players, annual_rosters, accolades
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    pre = response.content.decode().find("Pre-season second team All-American Outfielder")
    first = response.content.decode().find("First Team All-Conference")
    sec = response.content.decode().find("2nd team All-American Outfielder")
    assert sec < first
    assert first < pre


@pytest.mark.django_db
def test_single_player_page_renders_summer_accolades_in_summer_ball_section(
    client,
    players,
    annual_rosters,
    accolades,
    summer_assign,
    summer_leagues,
    summer_teams,
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.ryan_kraft.pk],
        )
    )
    assert response.status_code == 200
    assert "Ryan Kraft" in response.content.decode()
    summer_ball_section = parse_response(response).find(id="summer-ball")
    assert "Northwoods League Pitcher of the Year" in summer_ball_section.get_text()
