from django.urls import path

from mask.stores import views

app_name = "stores"
urlpatterns = [
    path("", views.dummy_view, name="dummy"),
]
