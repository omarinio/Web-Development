from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_view, name="category_view"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:id>/bid", views.bid, name="bid"),
    path("listing/<int:id>/add_comment", views.add_comment, name="comment"),
    path("listing/<int:id>/watchlist_add", views.add_watchlist, name="add_watchlist"),
    path("listing/<int:id>/watchlist_delete", views.delete_watchlist, name="delete_watchlist"),
    path("listing/<int:id>/close_listing", views.close_listing, name="close_listing")
]
