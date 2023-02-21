from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("listing/<str:listing>", views.listing, name="listing"),
    path("listing/<str:listing>/bid", views.bid, name="bid"),
    path("listing/<str:listing>/watchlist", views.alter_watchlist, name="alter_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<str:listing>/close", views.close_listing, name="close_listing"),
    path("listing/<str:listing>/comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories") 

]