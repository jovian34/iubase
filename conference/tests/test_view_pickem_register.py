import pytest

from django import urls

from accounts.tests.fixtures import logged_user_schwarbs, user_not_logged_in, random_guy
from conference.logic import year
from conference import models as conf_models


@pytest.mark.django_db
def test_pickem_register_redirects_not_logged_in(client, user_not_logged_in):
    response = client.get(urls.reverse("pickem_register", args=[year.get_this_year()]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_pickem_register_renders_template(client, logged_user_schwarbs):
    response = client.get(urls.reverse("pickem_register", args=[year.get_this_year()]))
    assert response.status_code == 200
    assert "Conditions and Privacy Notice" in response.content.decode()


@pytest.mark.django_db
def test_pickem_register_get_renders_form(client, random_guy):
    response = client.get(urls.reverse("pickem_register", args=[year.get_this_year()]))
    assert response.status_code == 200
    assert "Type a name or handle for your account" in response.content.decode()
    assert "Do you agree to the terms and conditions listed below?" in response.content.decode()
    assert "Do you want to be listed publicly this season?" in response.content.decode()


@pytest.mark.django_db
def test_pickem_register_post_saves_data(client, random_guy):
    response = client.post(
        urls.reverse("pickem_register", args=[year.get_this_year()]),
        {
            "display_name": "B1GBruce",
            "agree_to_terms": "on",
            "make_public": "on",
        },
        follow=True,
    )
    assert response.status_code == 200
    registration = conf_models.PickemRegisterAnnual.objects.get(
        user=random_guy,
        spring_year=year.get_this_year(),
    )
    assert registration.display_name == "B1GBruce"
    assert registration.agree_to_terms
    assert registration.make_public
    assert registration.spring_year == year.get_this_year()


@pytest.mark.django_db
def test_pickem_register_post_redirects_to_my_pickem(client, random_guy):
    response = client.post(
        urls.reverse("pickem_register", args=[year.get_this_year()]),
        {
            "display_name": "B1GBruce",
            "agree_to_terms": "on",
            "make_public": "on",
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Welcome, Bruce!" in response.content.decode()
    assert f"My {year.get_this_year()} Pick&#x27;em" in response.content.decode()
