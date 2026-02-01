import pytest
from collections import namedtuple
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


@pytest.fixture
def superuser_houston(client):
    houston = CustomUser.objects.create_user(
        username="jhouston",
        first_name="Jeremy",
        last_name="Houston",
        password="dbwrwbrj7499677693skjhkasH72!",
        is_superuser=True,
    )
    client.login(
        username="jhouston",
        password="dbwrwbrj7499677693skjhkasH72!",
    )
    return houston


@pytest.fixture
def staff_josh(client):
    houston = CustomUser.objects.create_user(
        username="jbennett",
        first_name="Josh",
        last_name="Bennett",
        password="dbwrwbrj7499677693skjhkasH72!",
        is_superuser=True,
    )
    client.login(
        username="jbennett",
        password="dbwrwbrj7499677693skjhkasH72!",
    )
    return staff_josh


@pytest.fixture
def staff_cass(client):
    houston = CustomUser.objects.create_user(
        username="crpalmer",
        first_name="Cassady",
        last_name="Palmer",
        password="dbwrwbrj7499677693skjhkasH72!",
        is_superuser=True,
    )
    client.login(
        username="crpalmer",
        password="dbwrwbrj7499677693skjhkasH72!",
    )
    return staff_cass


@pytest.fixture
def staff_chris(client):
    houston = CustomUser.objects.create_user(
        username="cfeeny",
        first_name="Chris",
        last_name="Feeny",
        password="dbwrwbrj7499677693skjhkasH72!",
        is_superuser=True,
    )
    client.login(
        username="cfeeny",
        password="dbwrwbrj7499677693skjhkasH72!",
    )
    return staff_chris


@pytest.fixture
def random_guy(client):
    houston = CustomUser.objects.create_user(
        username="bruce",
        first_name="Bruce",
        last_name="Random",
        password="dbwrwbrj7499677693skjhkasH72!",
        is_superuser=False,
    )
    client.login(
        username="bruce",
        password="dbwrwbrj7499677693skjhkasH72!",
    )
    return random_guy


@pytest.fixture
def user_forms(client):
    new_user = {
        "email": "newuser@email.com",
        "password": "Hdbwrwbrj72yu39293skjhkasH72"
    }
    FormObj = namedtuple(
        "FormObj",
        "new_user"
    )
    return FormObj(new_user=new_user)