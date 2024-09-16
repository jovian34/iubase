from django import apps


# django_project exists as an app so that custom templatetags get added
class DjangoProjectConfig(apps.AppConfig):
    name = "django_project"
