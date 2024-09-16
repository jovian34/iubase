from django import shortcuts
from django.contrib.auth import decorators
from datetime import datetime
import pytz

from index import models as index_models

timezone = pytz.timezone('US/Eastern')


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


@decorators.login_required
def last_months_traffic(request):
    first_of_month = get_first_of_current_month()
    traf = index_models.TrafficCounter.objects.filter(timestamp__lt=first_of_month)
    traf.delete()
    return shortcuts.redirect(index)


@decorators.login_required
def current_months_traffic(request):
    first_of_month = get_first_of_current_month()
    traf = index_models.TrafficCounter.objects.filter(timestamp__gte=first_of_month).order_by(
        "-timestamp"
    )
    agent_info = AgentInfo()
    for row in traf:
        row.agent_group = agent_info.categorize_user_agent(row)
    context = {
        "traffic": traf,
        "count": len(traf),
        "title": "Last Month's Traffic",
    }
    return shortcuts. render(request, "index/one_months_traffic.html", context=context)


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


class AgentInfo():
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
        self.ios = ["iphone", "ipad",]
        self. linux_comp = ["linux x86", "linux i686",]


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