from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

from index.models import TrafficCounter


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def save_traffic_data(request, page):
    if not request.user.is_authenticated:
        traffic = TrafficCounter.objects.create(
                page=page,
                ip=get_client_ip(request),
                user_agent=request.headers.get("user-agent"),
            )
        traffic.save()


def index(request):              
    save_traffic_data(request, page="Main Index")
    return render(request, "index/index.html")


def categorize_user_agent(row):
    user_agent = (str(row.user_agent).lower())
    bots = ["bot", "newspaper", "go-http", "facebookexternalhit", "spider", "expanse", "internetmeasurement", "censys", "crawler", "python-requests", "curl", "java", "odin"]
    if any(bot in user_agent for bot in bots):
        category = "bot"
    elif "iphone" in user_agent or "ipad" in user_agent:
        category = "iPhone"
    elif "android" in user_agent:
        category = "Android"
    elif "linux x86" in user_agent:
        category = "Linux"
    elif "macintosh" in user_agent:
        category = "Mac"
    elif "windows" in user_agent:
        category = "PC"
    else:
        category = "other"
    return category


@login_required
def last_months_traffic(request):
    first_of_month = datetime(
        year=datetime.today().year,
        month=datetime.today().month,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    traf = TrafficCounter.objects.filter(timestamp__lt=first_of_month)
    traf.delete()
    return redirect(index)


@login_required
def current_months_traffic(request):
    first_of_month = datetime(
        year=datetime.today().year,
        month=datetime.today().month,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    traf = TrafficCounter.objects.filter(timestamp__gte=first_of_month).order_by("-timestamp")
    for row in traf:
        row.agent_group = categorize_user_agent(row)
    context = {
        "traffic": traf,
        "count": len(traf),
        "title": "Last Month's Traffic",
    }
    return render(request, "index/one_months_traffic.html", context=context)
