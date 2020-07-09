from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("falito", views.falito, name="falito"),
    path("<str:name>", views.greet, name="greet")
]