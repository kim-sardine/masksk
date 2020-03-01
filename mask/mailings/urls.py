from django.urls import path

from mask.mailings import views

app_name = "mailings"
urlpatterns = [
    path("create/", views.create_mailing, name="create-mailing"),
    path("revoke/<str:token>/", views.revoke_mailing, name="revoke"),
]
