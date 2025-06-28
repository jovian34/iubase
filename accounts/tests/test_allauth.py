from django.contrib import auth
from django import shortcuts, urls
import pytest

from accounts.tests.fixtures import user_forms
from accounts import models as acct_models

@pytest.mark.django_db
def test_allauth_signup_page_renders(client):
    response = client.get(urls.reverse("account_signup"), follow=True)
    assert response.status_code == 200
    assert "Your password must contain at least 8 characters." in str(response.content)


@pytest.mark.django_db
def test_new_user_created(client, user_forms):
    response = client.post(
        urls.reverse("account_signup"), 
        user_forms.new_user,
        follow=True
    )
    assert response.status_code == 200
    assert f"{user_forms.new_user['email']}" in str(response.content)
