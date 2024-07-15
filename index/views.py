from django.shortcuts import render

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
