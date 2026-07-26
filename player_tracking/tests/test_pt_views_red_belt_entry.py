import pytest
from django.urls import reverse

from accounts.tests.fixtures import logged_user_schwarbs


@pytest.mark.django_db
def test_red_belt_entry_page_renders(admin_client):
    response = admin_client.get(reverse("red_belt_entry"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_red_belt_entry_page_redirects_not_logged_in(client):
    response = client.get(reverse("red_belt_entry"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_red_belt_entry_page_asks_for_password_not_logged_in(client):
    response = client.get(reverse("red_belt_entry"), follow=True)
    assert response.status_code == 200
    assert "Sign In Via Google" in response.content.decode()


@pytest.mark.django_db
def test_red_belt_entry_page_forbidden_without_add_accolade_permission(
    client, logged_user_schwarbs
):
    response = client.get(reverse("red_belt_entry"))
    assert response.status_code == 403
    assert "Forbidden Error Recorded" in response.content.decode()
