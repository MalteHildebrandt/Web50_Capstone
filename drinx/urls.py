from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("backend", views.backend_index, name="backend_index"),
    path("backend/categories", views.backend_categories, name="backend_categories"),
    path("backend/articles", views.backend_articles, name="backend_articles"),

    #api urls
    path("savecategory", views.savecategory, name="savecategory")
    
]