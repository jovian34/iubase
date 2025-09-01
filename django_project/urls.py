from django.contrib import admin
from django.urls import include, path
from django.views.generic import base
import os
from django_project import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "robots.txt", 
        base.TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("index/", include("index.urls")),
    path("accounts/", include("allauth.urls")),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("conference/", include("conference.urls"), name="conference"),
    path("live_game_blog/", include("live_game_blog.urls"), name="live_game_blog"),
    path("player_tracking/", include("player_tracking.urls"), name="player_tracking"),
    path(f"{os.getenv('ADMIN_WORD')}/", admin.site.urls),
]

admin.site.site_header = "apps_iubase"
admin.site.site_title = "apps_iubase"
admin.site.index_title = "apps_iubase"
