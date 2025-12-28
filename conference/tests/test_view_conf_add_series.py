import pytest

from django import urls


@pytest.mark.django_db
def test_add_series_get_renders(admin_client):
    response = admin_client.get(urls.reverse("add_series"))
    assert response.status_code == 200