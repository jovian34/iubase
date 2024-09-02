import pytest

from collections import namedtuple


@pytest.fixture
def forms():
    pfw = {
        "team_name": "Purdue Ft. Wayne",
        "mascot": "Mastodons",
        "logo": "https://cdn.d1baseball.com/uploads/2023/12/21143914/iupufw.png",
        "stats": "https://d1baseball.com/team/iupufw/stats/",
        "roster": "https://gomastodons.com/sports/baseball/roster",
    }
    FormObj = namedtuple(
        "FormObj",
        "pfw",
    )
    return FormObj(
        pfw=pfw,
    )