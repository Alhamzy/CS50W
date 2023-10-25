from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.view_entry, name="entry"),
    path("new_entry/", views.new_entry, name = "new_entry"),
    path("random_entry/", view.random_entry, name = "random_entry")
]
