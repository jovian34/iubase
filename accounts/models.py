from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    x_prof = models.URLField(null=True, blank=True)
