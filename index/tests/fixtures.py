import pytest

from collections import namedtuple
from datetime import datetime, timedelta

from index import models as index_models


@pytest.fixture
def agents():
    windows = index_models.TrafficCounter.objects.create(
        page="Main Index",
        timestamp=datetime.today().astimezone() - timedelta(seconds=3),
        ip="127.0.0.1",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    )
    bot = index_models.TrafficCounter.objects.create(
        page="2024-04-14 17:04 Penn State at Indiana",
        timestamp=datetime.today().astimezone() - timedelta(seconds=15),
        ip="47.128.55.115",
        user_agent="Mozilla/5.0 (compatible; Bytespider; spider-feedback@bytedance.com) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.0.0 Safari/537.36",
    )
    mac = index_models.TrafficCounter.objects.create(
        page="2024 Transfer Portal",
        timestamp=datetime.today().astimezone() - timedelta(seconds=25),
        ip="45.16.203.44",
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    )
    iphone = index_models.TrafficCounter.objects.create(
        page="AJ Shepard",
        timestamp=datetime.today().astimezone() - timedelta(seconds=35),
        ip="104.139.10.207",
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
    )
    android = index_models.TrafficCounter.objects.create(
        page="AJ Shepard",
        timestamp=datetime.today().astimezone() - timedelta(seconds=37),
        ip="72.14.201.229",
        user_agent="Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.69 Mobile Safari/537.36",
    )
    last_mo_yr, last_mo_mo = set_last_year_month()
    last_month = index_models.TrafficCounter.objects.create(
        page="AJ Shepard",
        timestamp=datetime(
            year=last_mo_yr,
            month=last_mo_mo,
            day=8,
            hour=10,
            minute=38,
            second=27,
        ).astimezone(),
        ip="104.139.10.207",
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
    )
    AgentObj = namedtuple(
        "AgentObj",
        "windows bot mac iphone android last_month"
    )
    return AgentObj(
        windows=windows,
        bot=bot,
        mac=mac,
        iphone=iphone,
        android=android,
        last_month=last_month,
    )

def set_last_year_month():
    # handles edge case where last month is December of last year
    if datetime.today().month == 1:
        last_mo_yr = datetime.today().year - 1
        last_mo_mo = 12
    else:
        last_mo_yr = datetime.today().year
        last_mo_mo = datetime.today().month - 1
    return last_mo_yr,last_mo_mo