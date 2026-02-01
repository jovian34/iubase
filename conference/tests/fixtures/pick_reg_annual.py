import pytest
from collections import namedtuple

from conference import models as conf_models
from conference.logic import year
from accounts.tests.fixtures import staff_josh, staff_chris, staff_cass, superuser_houston, logged_user_schwarbs


@pytest.fixture
def pick_reg_annual(staff_josh, staff_chris):
    josh = conf_models.PickemRegisterAnnual.objects.create(
        user = staff_josh,
        spring_year = year.get_this_year(),
        display_name = "The Founder",
        is_staff = True,
        agree_to_terms = True,
        make_public = True,
    )
    chris = conf_models.PickemRegisterAnnual.objects.create(
        user = staff_chris,
        spring_year = year.get_this_year(),
        display_name = "Mr. Met",
        is_staff = True,
        agree_to_terms = True,
        make_public = True,
    )
    cass = conf_models.PickemRegisterAnnual.objects.create(
        user = staff_cass,
        spring_year = year.get_this_year(),
        display_name = "Stats Guru",
        is_staff = True,
        agree_to_terms = True,
        make_public = True,
    )
    houston = conf_models.PickemRegisterAnnual.objects.create(
        user = superuser_houston,
        spring_year = year.get_this_year(),
        display_name = "Jeremy",
        is_staff = False,
        agree_to_terms = True,
        make_public = False,
    )
    schwarbs = conf_models.PickemRegisterAnnual.objects.create(
        user = logged_user_schwarbs,
        spring_year = year.get_this_year(),
        display_name = "Schwarbomb",
        is_staff = False,
        agree_to_terms = True,
        make_public = True,
    )
    registrants = [
        "josh",
        "chris",
        "cass",
        "houston",
        "schwarbs",
    ]
    PickRegAnnualObj = namedtuple(
        "PickRegAnnualObj",
        registrants,
    )
    return PickRegAnnualObj(
        josh=josh,
        chris=chris,
        cass=cass,
        houston=houston,
        schwarbs=schwarbs,
    )
                                                                                                                                                                                                                                                                                                                                                                            