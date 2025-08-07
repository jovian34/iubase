import pytest

from conference.tests.fixtures.conferences import conferences


@pytest.mark.django_db
def test_conf_model_stored_abbreviation_and_long_name(client, conferences):
    assert conferences.b1g.abbrev == "B1G"
    assert conferences.sec.long_name == "Southeastern Conference"



@pytest.mark.django_db
def test_conf_model_renders_abbrev_as_string(client, conferences):
    assert str(conferences.b1g) == "B1G"