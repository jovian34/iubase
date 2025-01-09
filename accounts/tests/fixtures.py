import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import CustomUser
from live_game_blog import models as lgb_models


@pytest.fixture
def user_not_logged_in(client):
    denato = CustomUser.objects.create_user(
        username="denato",
        first_name="Joey",
        last_name="DeNato",
        password="Hdbwrwbrj72478593skjhkasH72!",
    )
    return denato


@pytest.fixture
def user_iubase17(client):
    iubase17 = CustomUser.objects.create_user(
        username="iubase17",
        first_name="@iubase17",
        last_name="",
        password="Idbwrwbrj72478593skjhkasH72!",
    )
    return iubase17


@pytest.fixture
def logged_user_schwarbs(client):
    schwarber = CustomUser.objects.create_user(
        username="schwarber",
        first_name="Kyle",
        last_name="Schwarber",
        password="Hdbwrwbrj7239293skjhkasH72!",
    )
    client.login(
        username="schwarber",
        password="Hdbwrwbrj7239293skjhkasH72!",
    )
    return schwarber
