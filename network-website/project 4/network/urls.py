
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost",views.newpost, name="newpost"),
    path("profiles/<int:id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("like/<int:id>", views.like, name="like"),
    path("editprofile/<int:id>", views.editprofile, name="editprofile"),
    path("main", views.main, name="main")
]
