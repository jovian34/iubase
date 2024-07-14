from django.db import models
from django.db.models.functions import Now


class TrafficCounter(models.Model):
    page = models.CharField(null=False, max_length=128)
    timestamp = models.DateTimeField(db_default=Now())
    ip = models.CharField(null=True, max_length=256)
    user_agent = models.CharField(null=True, max_length=128)

    def __str__(self) -> str:
        return f"{self.timestamp}"
