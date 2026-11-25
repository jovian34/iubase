import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.form_data import forms
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.logic import player_props
from player_tracking.models import AnnualRoster, Player, Transaction
from live_game_blog.tests.fixtures.teams import teams
from accounts.models import CustomUser
from accounts.tests.fixtures import logged_user_schwarbs


this_year = date.today().year


@pytest.mark.django_db
def test_set_player_properties_forbidden_without_perms(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"),)
    assert response.status_code == 403


@pytest.mark.django_db
def test_set_player_properties_html_uses_old_rule_dates(admin_client):
    player = Player.objects.create(first="Old", last="Rules", hsgrad_year=2020)
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2019, 6, 1),
    )

    response = admin_client.get(reverse("set_player_properties"), follow=True)

    assert response.status_code == 200
    assert "2021-2024" in response.content.decode()
    assert "Old Rules" in response.content.decode()


@pytest.mark.django_db
def test_set_player_properties_html_uses_transition_dates(admin_client):
    player = Player.objects.create(first="Transition", last="Rules", hsgrad_year=2024)
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2023, 6, 1),
    )

    response = admin_client.get(reverse("set_player_properties"), follow=True)

    assert response.status_code == 200
    assert "2025-2029" in response.content.decode()
    assert "Transition Rules" in response.content.decode()


@pytest.mark.django_db
def test_mid_year_transfer_ends_eligibility_in_next_spring():
    player = Player.objects.create(first="Midyear", last="Transfer", hsgrad_year=2022)
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2020, 9, 26),
    )
    Transaction.objects.create(
        player=player,
        trans_event="Entered Transfer Portal",
        trans_date=date(2022, 12, 11),
    )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2023
    assert player.last_spring == 2023
    assert not player.via_exhaust


@pytest.mark.django_db
def test_set_player_properties_correctly_marks_via_exhaust(
    admin_client, players, annual_rosters, transactions
):
    response = admin_client.get(reverse("players"), follow=True)
    evan_mac = Player.objects.get(pk=players.evan_mac.pk)
    cole_gilley = Player.objects.get(pk=players.cole_gilley.pk)
    assert evan_mac.via_exhaust
    assert cole_gilley.via_exhaust
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    evan_mac = Player.objects.get(pk=players.evan_mac.pk)
    cole_gilley = Player.objects.get(pk=players.cole_gilley.pk)
    assert not evan_mac.via_exhaust
    assert cole_gilley.via_exhaust


@pytest.mark.django_db
def test_future_commit_gets_five_years_under_new_rules():
    player = Player.objects.create(
        first="Future",
        last="Commit",
        hsgrad_year=2027,
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2026, 8, 6),
    )
    Transaction.objects.create(
        player=player,
        trans_event="National Letter of Intent Signed",
        trans_date=date(2027, 11, 25),
    )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2028
    assert player.last_spring == 2032


@pytest.mark.django_db
def test_drafted_player_ends_eligibility_in_draft_year():
    player = Player.objects.create(
        first="Drafted",
        last="Player",
        hsgrad_year=2023,
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2022, 6, 7),
    )
    for spring_year in (2024, 2025, 2026):
        AnnualRoster.objects.create(
            spring_year=spring_year,
            player=player,
            status="Spring Roster",
            primary_position="Pitcher",
        )
    Transaction.objects.create(
        player=player,
        trans_event="Drafted",
        trans_date=date(2026, 7, 15),
    )
    Transaction.objects.create(
        player=player,
        trans_event="Signed Professional Contract",
        trans_date=date(2026, 7, 21),
    )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2024
    assert player.last_spring == 2026


@pytest.mark.django_db
def test_old_rules_limit_redshirt_years():
    """
    The player uses one redshirt and receives one clock waiver. A second
    ordinary redshirt does not add another year under the old rules.
    """
    player = Player.objects.create(
        first="Jack",
        last="Moffitt",
        hsgrad_year=2021,
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2020, 6, 1),
    )
    roster_statuses = (
        "On Spring Roster but did not play",
        "Redshirt with clock extension - Medical",
        "On Spring Roster but did not play",
        "Spring Roster",
        "Spring Roster",
    )
    for offset, status in enumerate(roster_statuses):
        AnnualRoster.objects.create(
            spring_year=2022 + offset,
            player=player,
            status=status,
            primary_position="Pitcher",
        )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2022
    assert player.last_spring == 2027


@pytest.mark.django_db
def test_old_rules_first_year_greyshirt_adds_one_year_of_eligibility():
    player = Player.objects.create(
        first="Grey",
        last="Shirt",
        hsgrad_year=2020,
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2019, 6, 1),
    )
    roster_statuses = (
        "Not on Spring roster",
        "Spring Roster",
        "Spring Roster",
        "Spring Roster",
    )
    for year_offset, status in enumerate(roster_statuses):
        AnnualRoster.objects.create(
            spring_year=2021 + year_offset,
            player=player,
            status=status,
            primary_position="Pitcher",
        )
    player_props.set_player_props_get_errors()
    player.refresh_from_db()
    assert player.first_spring == 2021
    assert player.last_spring == 2025


@pytest.mark.django_db
def test_new_rules_give_first_time_entrant_five_years_to_play():
    player = Player.objects.create(
        first="Five",
        last="ForFive",
        hsgrad_year=2026,
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2026, 6, 1),
    )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2027
    assert player.last_spring == 2031


@pytest.mark.django_db
def test_new_rules_allow_playing_in_all_five_eligible_years():
    player = Player.objects.create(
        first="Five",
        last="Seasons",
        hsgrad_year=2026,
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2026, 6, 1),
    )
    for spring_year in range(2027, 2032):
        AnnualRoster.objects.create(
            spring_year=spring_year,
            player=player,
            status="Spring Roster",
            primary_position="Pitcher",
        )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2027
    assert player.last_spring == 2031


@pytest.mark.django_db
def test_transition_entrant_uses_better_result_when_old_eligibility_remains():
    player = Player.objects.create(
        first="Transition",
        last="Entrant",
        hsgrad_year=2025,
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2025, 6, 1),
    )
    AnnualRoster.objects.create(
        spring_year=2026,
        player=player,
        status="Spring Roster",
        primary_position="Pitcher",
    )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2026
    assert player.last_spring == 2030


@pytest.mark.django_db
def test_transition_entrant_keeps_longer_old_rule_eligibility():
    player = Player.objects.create(
        first="OldRule",
        last="Waivers",
        hsgrad_year=2025,
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2025, 6, 1),
    )
    roster_statuses = (
        "Redshirt with clock extension - Medical",
        "Spring Roster",
        "Redshirt with clock extension - Other",
        "Spring Roster",
    )
    for offset, status in enumerate(roster_statuses):
        AnnualRoster.objects.create(
            spring_year=2026 + offset,
            player=player,
            status=status,
            primary_position="Pitcher",
        )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2026
    assert player.last_spring == 2031


@pytest.mark.django_db
def test_transition_entrant_with_final_old_season_gets_no_extra_eligibility():
    player = Player.objects.create(
        first="Final",
        last="Season",
        hsgrad_year=2022,
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2021, 6, 1),
    )
    for spring_year in range(2023, 2027):
        AnnualRoster.objects.create(
            spring_year=spring_year,
            player=player,
            status="Spring Roster",
            primary_position="Pitcher",
        )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2023
    assert player.last_spring == 2026


@pytest.mark.django_db
def test_player_who_becomes_staff_ends_eligibility_that_spring():
    player = Player.objects.create(first="Former", last="Player", hsgrad_year=2025)
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2024, 3, 17),
    )
    Transaction.objects.create(
        player=player,
        trans_event="Not playing but with the program in another role",
        trans_date=date(2026, 2, 15),
    )
    AnnualRoster.objects.create(
        spring_year=2026,
        player=player,
        status="Not on Spring roster",
        primary_position="Pitcher",
    )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2026
    assert player.last_spring == 2026
    assert not player.via_exhaust


@pytest.mark.django_db
def test_set_player_properties_produces_correct_end_date_redshirt_transfer(
    admin_client, players, annual_rosters, transactions
):
    response = admin_client.get(reverse("players"), follow=True)
    cole = Player.objects.get(pk=players.cole_gilley.pk)
    assert not cole.first_spring or cole.last_spring
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    cole = Player.objects.get(pk=players.cole_gilley.pk)
    assert cole.first_spring == this_year + 1
    assert cole.last_spring == this_year + 1


@pytest.mark.django_db
def test_portal_entry_ends_eligibility_immediately():
    player = Player.objects.create(first="Portal", last="Player", hsgrad_year=2023)
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from College",
        trans_date=date(2025, 7, 15),
    )
    Transaction.objects.create(
        player=player,
        trans_event="Entered Transfer Portal",
        trans_date=date(2026, 6, 15),
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment to Transfer College",
        trans_date=date(2026, 7, 8),
    )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2026
    assert player.last_spring == 2026
    assert not player.via_exhaust


@pytest.mark.django_db
def test_set_player_properties_properly_resets_drafted_not_signed(
    admin_client, players, annual_rosters, transactions
):
    response = admin_client.get(reverse("players"), follow=True)
    grant = Player.objects.get(pk=players.grant_hollister.pk)
    assert not grant.first_spring or grant.last_spring
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    grant = Player.objects.get(pk=players.grant_hollister.pk)
    assert grant.first_spring == this_year + 1
    assert grant.last_spring == this_year + 5


@pytest.mark.django_db
def test_missing_annual_roster_error_uses_local_player_data(admin_client):
    player = Player.objects.create(
        first="Missing",
        last="Roster",
        hsgrad_year=2022,
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2021, 6, 1),
    )
    for spring_year in (2023, 2025):
        AnnualRoster.objects.create(
            spring_year=spring_year,
            player=player,
            status="Spring Roster",
            primary_position="Pitcher",
        )

    response = admin_client.get(reverse("set_player_properties"), follow=True)

    assert response.status_code == 200
    assert "missing roster year 2024 for Missing Roster" in str(response.content)


@pytest.mark.django_db
def test_early_juco_commit_uses_old_rule_dates():
    player = Player.objects.create(first="Old", last="Juco", hsgrad_year=2020)
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from College",
        trans_date=date(2020, 8, 23),
    )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2021
    assert player.last_spring == 2024


@pytest.mark.django_db
def test_early_juco_commit_uses_transition_dates():
    player = Player.objects.create(first="Transition", last="Juco", hsgrad_year=2024)
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from College",
        trans_date=date(2024, 8, 23),
    )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2025
    assert player.last_spring == 2029


@pytest.mark.django_db
def test_transition_juco_eligibility_start_uses_roster_not_team_start():
    player = Player.objects.create(
        first="Juco",
        last="Transfer",
        hsgrad_year=2024,
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from College",
        trans_date=date(2025, 10, 23),
    )
    for spring_year in (2025, 2026):
        AnnualRoster.objects.create(
            spring_year=spring_year,
            player=player,
            status="Spring Roster",
            primary_position="Pitcher",
        )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2027
    assert player.last_spring == 2029


@pytest.mark.django_db
def test_set_player_properties_properly_sets_no_starts_for_decommit(
    client,
    players,
    annual_rosters,
    transactions,
):
    sinke = Player.objects.get(pk=players.gibson_sinke.pk)
    assert not sinke.first_spring or sinke.last_spring
    player_props.set_player_props_get_errors()
    sinke = Player.objects.get(pk=players.gibson_sinke.pk)
    assert not sinke.first_spring or sinke.last_spring


@pytest.mark.django_db
def test_set_player_properties_properly_sets_no_starts_for_future_year_decommit(
    client,
    players,
    annual_rosters,
    transactions,
):
    amalbert = Player.objects.get(pk=players.jason_amalbert.pk)
    assert not amalbert.first_spring
    assert not amalbert.last_spring
    assert amalbert.first == "Jason"
    player_props.set_player_props_get_errors()
    amalbert = Player.objects.get(pk=players.jason_amalbert.pk)
    assert amalbert.first == "Jason"
    assert amalbert.first_spring == None
    assert amalbert.last_spring == None


@pytest.mark.django_db
def test_set_player_properties_asks_for_password_not_logged_in(
    client, players, annual_rosters, transactions
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    assert "Sign In Via Google" in response.content.decode()


@pytest.mark.django_db
def test_set_player_properties_produces_correct_end_date_typical_case(
    admin_client, players, annual_rosters, transactions
):
    krafty = Player.objects.get(pk=players.ryan_kraft.pk)
    assert not krafty.first_spring or krafty.last_spring
    player_props.set_player_props_get_errors()
    krafty = Player.objects.get(pk=players.ryan_kraft.pk)
    assert krafty.first_spring == this_year - 2
    assert krafty.last_spring == this_year + 2


@pytest.mark.django_db
def test_draft_ranked_player_keeps_old_rule_end_date():
    """
    This app used to show an end date based on projected draft ranking, but
    we are not doing that anymore
    """
    player = Player.objects.create(first="Old", last="Drafted", hsgrad_year=2020)
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2019, 6, 1),
    )
    Transaction.objects.create(
        player=player,
        trans_event="Ranked MLB Draft Prospect for Next Draft",
        trans_date=date(2023, 12, 10),
    )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2021
    assert player.last_spring == 2024


@pytest.mark.django_db
def test_draft_ranked_player_keeps_transition_end_date():
    player = Player.objects.create(
        first="Transition", last="Drafted", hsgrad_year=2024
    )
    Transaction.objects.create(
        player=player,
        trans_event="Verbal Commitment from High School",
        trans_date=date(2023, 6, 1),
    )
    Transaction.objects.create(
        player=player,
        trans_event="Ranked MLB Draft Prospect for Next Draft",
        trans_date=date(2025, 12, 10),
    )

    player_props.set_player_props_get_errors()

    player.refresh_from_db()
    assert player.first_spring == 2025
    assert player.last_spring == 2029
