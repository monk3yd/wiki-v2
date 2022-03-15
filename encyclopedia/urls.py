from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="wiki"),
    path("wiki/<str:title>/", views.article, name="article"),
    path("create/", views.create, name="create"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random/", views.rand, name="random"),
]
