from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("filtered/<str:category>", views.filtered, name="filtered"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("watchList/<str:username>", views.watchList, name="watchList"),
    path(
        "filteredWatchList/<str:category>",
        views.filteredWatchList,
        name="filteredWatchList",
    ),
]
