import pytest
import os

from ..models import CustomUser


@pytest.fixture()
def user_1(db):
    user = CustomUser.objects.create_user("user_one")
    return user


def test_user_one_exists_in_db(user_1):
    assert user_1.username == "user_one"


def test_set_check_passphrase(user_1):
    user_1.set_password("This is my new passphrase")
    assert user_1.check_password("This is my new passphrase") is True
    assert user_1.check_password("This is NOT my new passphrase") is False


@pytest.mark.django_db
def test_admin_page_renders(client):
    response = client.get(f"/{os.getenv('ADMIN_WORD')}/", follow=True)
    assert response.status_code == 200
    assert "jovian34_iubase" in str(response.content)
