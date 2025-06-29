from django.contrib import auth
from django import shortcuts, urls
import pytest

from accounts.tests.fixtures import user_forms
from accounts import models as acct_models


@pytest.mark.django_db
def test_allauth_google_login_page_renders(client):
    response = client.get('/accounts/google/login/')
    assert response.status_code == 200
    assert "Continue" in str(response.content)
