from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_view, name="category_view"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:id>/bid", views.bid, name="bid"),
    path("listing/<int:id>/add_comment", views.add_comment, name="comment")
]
