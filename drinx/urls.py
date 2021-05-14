from django.urls import path
from . import views


urlpatterns = [
    #frontend urls
    path("", views.index, name="index"),
    path("articles/<int:category_id>", views.articles, name="articles"),
    path("cart", views.cart, name="cart"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),

    #backend urls
    path("backend", views.backend_index, name="backend_index"),
    path("backend/categories", views.backend_categories, name="backend_categories"),
    path("backend/articles/<int:category_id>", views.backend_articles, name="backend_articles"),

    #api urls
    path("savecategory", views.savecategory, name="savecategory"),
    path("articleAPI", views.articleAPI, name="articleAPI"),
    path("cartAPI", views.cartAPI, name="cartAPI")
    
]