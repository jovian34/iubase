from django.contrib import admin
from django.db import models
from index.models import TrafficCounter


@admin.register(TrafficCounter)
class TrafficCounterAdmin(admin.ModelAdmin):
    model = TrafficCounter
    list_display = (
        "page",
        "timestamp",
        "ip",
        "user_agent",
    )
