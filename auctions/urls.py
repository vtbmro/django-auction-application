from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("upload_listing", views.upload_listing, name="upload_listing"),
    path("<int:listing_id>", views.display_listing, name="listing"),
    path("a/<int:listing_id>", views.watchlist_add, name="watchlist_add"),
    path("d/<int:listing_id>", views.watchlist_delete, name="watchlist_delete"),
    path("comment/<int:listing_id>", views.publish_comment, name="publish_comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_especific, name="category_load"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("watchlist", views.watchlist, name="watchlist")
]
