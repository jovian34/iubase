from django import shortcuts, urls
from django.contrib.auth import decorators as auth_dec

from datetime import date

from player_tracking.models import Player, Transaction
from player_tracking.forms import NewPlayerForm
from player_tracking.views.set_player_properties import set_player_props_get_errors


@auth_dec.login_required
def view(request):
    if request.method == "POST":
        return validate_post_new_player_form_save_then_redirect(request)
    else:
        context = {
            "form": initialize_new_player_form(),
            "page_title": "Add a New Player",
        }
        template_path = "player_tracking/add_player.html"
        return shortcuts.render(request, template_path, context)


def validate_post_new_player_form_save_then_redirect(request):
    form = NewPlayerForm(request.POST)
    if form.is_valid():
        save_new_player_and_init_transaction(form)
        set_player_props_get_errors()
    return shortcuts.redirect(urls.reverse("players"))


def initialize_new_player_form():
    return NewPlayerForm(
        initial={
            "hsgrad_year": date.today().year,
            "home_country": "USA",
        },
    )


def save_new_player_and_init_transaction(form):
    save_new_player(form)
    save_initial_transaction(form)


def save_new_player(form):
    add_player = Player.objects.create(
        first=form.cleaned_data["first"],
        last=form.cleaned_data["last"],
        hsgrad_year=form.cleaned_data["hsgrad_year"],
        high_school=form.cleaned_data["high_school"],
        home_city=form.cleaned_data["home_city"],
        home_state=form.cleaned_data["home_state"],
        home_country=form.cleaned_data["home_country"],
        headshot=form.cleaned_data["headshot"],
        action_shot=form.cleaned_data["action_shot"],
        birthdate=form.cleaned_data["birthdate"],
        bats=form.cleaned_data["bats"],
        throws=form.cleaned_data["throws"],
        height=form.cleaned_data["height"],
        weight=form.cleaned_data["weight"],
        primary_position=form.cleaned_data["primary_position"],
    )
    add_player.save()


def save_initial_transaction(form):
    this_player = get_current_player(form)
    add_initial_transaction = Transaction(
        player=this_player,
        trans_event=form.cleaned_data["trans_event"],
        trans_date=form.cleaned_data["trans_date"],
        citation=form.cleaned_data["citation"],
        primary_position=form.cleaned_data["primary_position"],
    )
    add_initial_transaction.save()


def get_current_player(form):
    first = form.cleaned_data["first"]
    last = form.cleaned_data["last"]
    hsgrad_year = int(form.cleaned_data["hsgrad_year"])
    this_player = Player.objects.filter(
        first=first, last=last, hsgrad_year=hsgrad_year
    ).first()
    return this_player
