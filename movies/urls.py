from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.get_all_movies, name='all-movies'),
    path('movies/genre/<str:genre>/', views.get_movies_by_genre, name='movies-by-genre'),
    path('movies/featured/', views.get_featured_movies, name='featured-movies'),
]