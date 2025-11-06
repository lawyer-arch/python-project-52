from django.urls import path

from .views import (
    UsersListView,
    UsersCreateView,
    UsersUpdateView,
    UsersDeleteView
)

app_name = "users"

urlpatterns = [
    path(
        "",
        UsersListView.as_view(),
        name="users_list"
    ),
    path(
        "create/",
        UsersCreateView.as_view(),
        name="users_create"
    ),
    path(
        "<int:pk>/update/",
        UsersUpdateView.as_view(),
        name="users_update"
    ),
    path(
        "<int:pk>/delete/",
        UsersDeleteView.as_view(),
        name="users_delete"
    ),
]
