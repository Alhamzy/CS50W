from django.urls import path

from . import views,util
import random



app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_title>/", views.view_entry, name="view_entry"),
    path("new_entry/", views.new_entry, name = "new_entry"),
    path("random/", views.random_entry, name = "random_entry"),
    path("page_not_found/",views.page_not_found, name="page_not_found"),
    path("edit_description/<str:entry_title>", views.edit_entry, name = "edit_entry")
]
