from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories/<str:category>", views.categories, name="categories"),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('create/', views.create_listing, name='create'),
    path("listing/<int:id>/", views.listinge_page, name='listing'),
    path("all_listing/", views.active, name='active'),
    path('your_listing', views.your_listing, name='your_listing'),
    path('comment/<int:id>/', views.comment, name='comment'),
    path('bid/<int:id>/', views.make_bid, name='make_bid' )
]
