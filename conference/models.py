from django.db import models


class Conference(models.Model):
    abbrev = models.CharField(null=False, max_length=8, unique=True)
    long_name = models.CharField(null=False, max_length=64, unique=True)


    def __str__(self):
        return self.abbrev