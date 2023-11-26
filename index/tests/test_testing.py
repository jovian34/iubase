import pytest
from django.contrib.auth.models import User

def test_pytest_works():
    assert 1 == 1

@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('test', 'test@test.com', 'test')
    assert User.objects.count() == 1
