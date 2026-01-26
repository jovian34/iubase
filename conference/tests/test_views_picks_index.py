import pytest
import datetime

from django import urls


def test_picks_index_page_renders(client):
    response = client.get(urls.reverse("picks_index", args=[datetime.date.today().year]))
    assert response.status_code == 200
    assert f"{datetime.date.today().year} B1G Series Picks Home" in response.content.decode()