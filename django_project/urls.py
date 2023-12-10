from django.contrib import admin
from django.urls import include, path
import os
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(f"index/", include("index.urls")),
    path(f"live_game_blog/", include("live_game_blog.urls"), name="live_game_blog"),
    path(f"{os.getenv('ADMIN_WORD')}/", admin.site.urls),
]

admin.site.site_header = "jovian34_iubase"
admin.site.site_title = "jovian34_iubase"
admin.site.index_title = "jovian34_iubase"
