import pytest


def test_index_redirect(client):
    response = client.get("")
    assert response.status_code == 302


def test_redirect_goes_to_index(client):
    response = client.get("", follow=True)
    assert response.status_code == 200
    assert "Application Index" in str(response.content)
    assert "Live Game Blogs" in str(response.content)
    assert "Player Tracking" in str(response.content)
