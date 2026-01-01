import pytest
from django import urls
from datetime import datetime

from index.tests.fixtures import agents
from index import models as index_models
from accounts.tests.fixtures import logged_user_schwarbs


@pytest.mark.django_db
def test_index_renders(client):
    response = client.get(urls.reverse("index"))
    assert response.status_code == 200
    assert "Live Game Blogs" in response.content.decode()


@pytest.mark.django_db
def test_last_month_is_deleted(admin_client, agents):
    traffic = index_models.TrafficCounter.objects.all()
    initial_count = len(traffic)
    response = admin_client.get(urls.reverse("last_months_traffic"))
    assert response.status_code == 302
    traffic = index_models.TrafficCounter.objects.all()
    after_count = len(traffic)
    assert initial_count - after_count == 1


@pytest.mark.django_db
def test_last_month_is_not_deleted_user_not_logged_in(client, agents):
    traffic = index_models.TrafficCounter.objects.all()
    initial_count = len(traffic)
    response = client.get(urls.reverse("last_months_traffic"))
    assert response.status_code == 302
    traffic = index_models.TrafficCounter.objects.all()
    after_count = len(traffic)
    assert initial_count == after_count


@pytest.mark.django_db
def test_last_month_is_not_deleted_standard_user_logged_in(client, agents, logged_user_schwarbs):
    traffic = index_models.TrafficCounter.objects.all()
    initial_count = len(traffic)
    response = client.get(urls.reverse("last_months_traffic"))
    assert response.status_code == 302
    traffic = index_models.TrafficCounter.objects.all()
    after_count = len(traffic)
    assert initial_count == after_count


@pytest.mark.django_db
def test_index_hit_adds_traffic(client, agents):
    traffic = index_models.TrafficCounter.objects.all()
    initial_count = len(traffic)
    response = client.get(urls.reverse("index"))
    assert response.status_code == 200
    traffic = index_models.TrafficCounter.objects.all()
    after_count = len(traffic)
    assert after_count - initial_count == 1


@pytest.mark.django_db
def test_index_hit_adds_no_traffic_for_logged_in_user(
    client, agents, logged_user_schwarbs
):
    traffic = index_models.TrafficCounter.objects.all()
    initial_count = len(traffic)
    response = client.get(urls.reverse("index"))
    assert response.status_code == 200
    traffic = index_models.TrafficCounter.objects.all()
    after_count = len(traffic)
    assert after_count - initial_count == 0


@pytest.mark.django_db
def test_current_days_traffic_renders(admin_client, agents):
    day = datetime.today().day
    response = admin_client.get(urls.reverse("one_days_traffic", args=[day]))
    assert response.status_code == 200
    assert "47.128.55.115" in response.content.decode()
    assert "AJ Shepard" in response.content.decode()
    assert "iPhone" in response.content.decode()
    assert "Android" in response.content.decode()


@pytest.mark.django_db
def test_current_days_traffic_redirects_without_perms(client, agents, logged_user_schwarbs):
    day = datetime.today().day
    response = client.get(urls.reverse("one_days_traffic", args=[day]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_current_months_traffic_redirects_without_perms(client, agents, logged_user_schwarbs):
    response = client.get(urls.reverse("current_months_traffic"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_current_months_traffic_renders(admin_client, agents):
    response = admin_client.get(urls.reverse("current_months_traffic"))
    assert response.status_code == 200
    assert "Traffic for" in response.content.decode()


@pytest.mark.django_db
def test_current_months_traffic_redirects_not_logged_in(client, agents):
    response = client.get(urls.reverse("current_months_traffic"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_current_months_traffic_asks_for_password_not_logged_in(client, agents):
    response = client.get(urls.reverse("current_months_traffic"), follow=True)
    assert response.status_code == 200
    assert "Traffic Count" not in response.content.decode()
    assert "2024 Transfer Portal" not in response.content.decode()
    assert "Password:" in response.content.decode()
