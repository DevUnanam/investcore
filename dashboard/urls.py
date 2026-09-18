from django.urls import path

from . import views


app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/users/", views.users, name="users"),
    path("admin/users/create/", views.create_user, name="create_user"),
    path("admin/users/<int:user_id>/edit/", views.edit_user, name="edit_user"),
    path("admin/users/<int:user_id>/delete/", views.delete_user, name="delete_user"),
]
