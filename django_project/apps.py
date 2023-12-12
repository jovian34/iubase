from django.apps import AppConfig


# django_project exists as an app so that custom templatetags get added
class DjangoProjectConfig(AppConfig):
    name = "django_project"
