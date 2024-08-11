from django.urls import path
from index import views

urlpatterns = [
    path("", views.index, name="index"),
    path("last_months_traffic", views.last_months_traffic, name="last_months_traffic"),
]
