from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="wiki"),
    path("wiki/<str:title>/", views.article, name="article"),
    path("wiki/search/", views.search, name="search")
]
