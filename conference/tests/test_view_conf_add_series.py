import pytest
import datetime

from django import urls

spring_year = datetime.date.today().year
if datetime.date.today().month > 8:
    spring_year = spring_year + 1


@pytest.mark.django_db
def test_add_series_get_renders(admin_client):
    response = admin_client.get(urls.reverse("add_series", args=[spring_year]))
    assert response.status_code == 200
    assert f"Add {spring_year} Conference Series" in response.content.decode()


@pytest.mark.django_db
def test_add_series_get_is_forbidden_without_perms(client):
    response = client.get(urls.reverse("add_series", args=[spring_year]))
    assert response.status_code == 403