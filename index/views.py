from django import shortcuts
from django.core import mail
from django.contrib.auth import decorators as auth
from datetime import datetime
import pytz

from index import models as index_models

timezone = pytz.timezone("US/Eastern")


def index(request):
    save_traffic_data(request, page="Main Index")
    return shortcuts.render(request, "index/index.html")


def save_traffic_data(request, page):
    if not request.user.is_authenticated:
        traffic = index_models.TrafficCounter.objects.create(
            page=page,
            ip=get_client_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
        traffic.save()


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@auth.permission_required("index.delete_trafficcounter")
def last_months_traffic(request):
    first_of_month = get_first_of_current_month()
    traf = index_models.TrafficCounter.objects.filter(timestamp__lt=first_of_month)
    traf.delete()
    return shortcuts.redirect(index)


@auth.permission_required("index.view_trafficcounter")
def current_months_traffic(request):
    today = datetime.today()
    prior_day = today.day - 1
    context = {
        "title": "Last Month's Traffic",
        "month": f"{today:%B}",
        "day": f"{today:%-d}",
        "prior_day": prior_day,
    }
    return shortcuts.render(request, "index/one_months_traffic.html", context=context)


@auth.permission_required("index.view_trafficcounter")
def one_days_traffic(request, day):
    end, start = get_start_and_end_of_day(day)
    traf = index_models.TrafficCounter.objects.filter(
        timestamp__gte=start, timestamp__lte=end
    ).order_by("-timestamp")
    agent_info = AgentInfo()
    for row in traf:
        row.agent_group = agent_info.categorize_user_agent(row)
    context = {
        "traffic": traf,
        "count": len(traf),
        "month_day": f"{start:%B %-d}",
        "prior_day": int(day) - 1,
    }
    return shortcuts.render(
        request, "index/partials/one_days_traffic.html", context=context
    )


def get_start_and_end_of_day(day):
    unaware_end = datetime(
        year=datetime.today().year,
        month=datetime.today().month,
        day=int(day),
        hour=23,
        minute=59,
        second=59,
    )
    end = timezone.localize(unaware_end)
    unaware_start = datetime(
        year=datetime.today().year,
        month=datetime.today().month,
        day=int(day),
        hour=0,
        minute=0,
        second=0,
    )
    start = timezone.localize(unaware_start)
    return end, start


def get_first_of_current_month():
    first_of_month = datetime(
        year=datetime.today().year,
        month=datetime.today().month,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    first_of_month = timezone.localize(first_of_month)
    return first_of_month


class AgentInfo:
    def __init__(self) -> None:
        self.bots = [
            "bot",
            "newspaper",
            "go-http",
            "facebookexternalhit",
            "spider",
            "expanse",
            "internetmeasurement",
            "censys",
            "crawler",
            "python-requests",
            "curl",
            "java",
            "odin",
            "panscient",
            "owler",
        ]
        self.ios = [
            "iphone",
            "ipad",
        ]
        self.linux_comp = [
            "linux x86",
            "linux i686",
        ]

    def categorize_user_agent(self, row):
        user_agent = str(row.user_agent).lower()
        if any(bot in user_agent for bot in self.bots):
            category = "bot"
        elif any(bot in user_agent for bot in self.ios):
            category = "iPhone"
        elif "android" in user_agent:
            category = "Android"
        elif any(linux in user_agent for linux in self.linux_comp):
            category = "Linux"
        elif "macintosh" in user_agent:
            category = "Mac"
        elif "windows" in user_agent:
            category = "PC"
        else:
            category = "other"
        return category
