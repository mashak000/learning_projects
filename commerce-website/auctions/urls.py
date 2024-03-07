from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("close/<int:id>", views.close, name="close"),
    path("category", views.category, name="category"),
    path("MyWatchlist", views.MyWatchlist, name="MyWatchlist"),
    path("speccategory/<str:category>", views.speccategory, name="speccategory")
]
