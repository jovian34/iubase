import pytest
import os
from index import models as index_models


def test_index_redirect(client):
    response = client.get("")
    assert response.status_code == 302


@pytest.mark.django_db
def test_redirect_goes_to_index(client):
    response = client.get("", follow=True)
    assert response.status_code == 200
    assert "Application Index" in str(response.content)
    assert "Live Game Blogs" in str(response.content)
    assert "Player Tracking" in str(response.content)


def test_robot_dot_txt_renders(client):
    response = client.get("/robots.txt")
    assert "Perplexity-User" in str(response.content)
    assert response.status_code == 200
    assert response["content-type"] == "text/plain"


@pytest.mark.django_db
def test_django_admin_renders(admin_client):
    response = admin_client.get(f"/{os.getenv('ADMIN_WORD')}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_save_traffic_data_stores_fw_ip(client):
    response = client.get(
        "",
        follow=True,
        HTTP_X_FORWARDED_FOR="82.83.85.88",
    )
    assert response.status_code == 200
    last_traffic = index_models.TrafficCounter.objects.last()
    assert last_traffic.ip == "82.83.85.88"
