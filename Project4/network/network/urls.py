
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("users/<int:id>", views.user, name="user"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("edit", views.edit, name="edit"),
    path("like", views.like, name="like")
]
