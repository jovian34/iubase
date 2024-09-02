from player_tracking.models import AnnualRoster, Player, SummerAssign, Transaction


def save_new_player_and_init_transaction(form):
    add_player = Player.objects.create(
        first=form.cleaned_data["first"],
        last=form.cleaned_data["last"],
        hsgrad_year=form.cleaned_data["hsgrad_year"],
        high_school=form.cleaned_data["high_school"],
        home_city=form.cleaned_data["home_city"],
        home_state=form.cleaned_data["home_state"],
        home_country=form.cleaned_data["home_country"],
        headshot=form.cleaned_data["headshot"],
        birthdate=form.cleaned_data["birthdate"],
        bats=form.cleaned_data["bats"],
        throws=form.cleaned_data["throws"],
        height=form.cleaned_data["height"],
        weight=form.cleaned_data["weight"],
    )
    add_player.save()
    this_player = Player.objects.last()
    add_initial_transaction = Transaction(
        player=this_player,
        trans_event=form.cleaned_data["trans_event"],
        trans_date=form.cleaned_data["trans_date"],
        citation=form.cleaned_data["citation"],
        primary_position=form.cleaned_data["primary_position"],
    )
    add_initial_transaction.save()


def save_transaction_form(player_id, form):
    add_transaction = Transaction.objects.create(
        player=Player.objects.get(pk=player_id),
        trans_event=form.cleaned_data["trans_event"],
        trans_date=form.cleaned_data["trans_date"],
        citation=form.cleaned_data["citation"],
        primary_position=form.cleaned_data["primary_position"],
        other_team=form.cleaned_data["other_team"],
        prof_org=form.cleaned_data["prof_org"],
        draft_round=form.cleaned_data["draft_round"],
        bonus_or_slot=form.cleaned_data["bonus_or_slot"],
        comment=form.cleaned_data["comment"],
    )
    add_transaction.save()


def save_roster_year(player_id, form):
    add_roster = AnnualRoster.objects.create(
        spring_year=form.cleaned_data["spring_year"],
        team=form.cleaned_data["team"],
        player=Player.objects.get(pk=player_id),
        jersey=form.cleaned_data["jersey"],
        status=form.cleaned_data["status"],
        primary_position=form.cleaned_data["primary_position"],
        secondary_position=form.cleaned_data["secondary_position"],
    )
    add_roster.save()


def save_summer_assign(player_id, form):
    add_assign = SummerAssign.objects.create(
        player=Player.objects.get(pk=player_id),
        summer_year=form.cleaned_data["summer_year"],
        summer_league=form.cleaned_data["summer_league"],
        summer_team=form.cleaned_data["summer_team"],
        source=form.cleaned_data["source"],
        citation=form.cleaned_data["citation"],
    )
    add_assign.save()
