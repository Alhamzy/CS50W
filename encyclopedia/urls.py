from django.urls import path

from . import views,util
import random



app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_title>/", views.view_entry, name="view_entry"),
    path("new_entry/", views.new_entry, name = "new_entry"),
    path("random/", views.random_entry, name = "random_entry")
]
