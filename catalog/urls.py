from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import home, detalhes_filme

urlpatterns = [
    path("", home, name="home"),
    path("filme/<str:imdb_id>/", detalhes_filme, name="detalhes_filme"),
    path("logout/", LogoutView.as_view(next_page='/accounts/login/'), name="logout"),
]

