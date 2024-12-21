import pytest
from django import urls
from datetime import date

from index.tests.fixtures import agents
from index import models as index_models
from accounts.tests.fixtures import logged_user_schwarbs

this_year = date.today().year


@pytest.mark.django_db
def test_traffic_counter_model_string(client, agents, logged_user_schwarbs):
    assert str(this_year) in str(agents.iphone)