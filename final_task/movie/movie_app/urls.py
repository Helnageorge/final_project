
from django.urls import path
from . import views

app_name = 'movie_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('all_latest_movies/', views.all_latest_movies, name='all_latest_movies'),
    path('all_upcoming_movies/', views.all_upcoming_movies, name='all_upcoming_movies'),
    path('add_review/', views.add_review, name='add_review'),
    path('add/', views.add, name='add_movie'),
    path('movies_by_genre/<int:genre_id>/', views.movies_by_genre, name='movies_by_genre'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search_movie, name='search_movie'),
    path('movie/<int:pk>/edit/', views.edit_movie, name='edit_movie'),
    path('movie/<int:pk>/delete/', views.delete_movie, name='delete_movie'),
    path('review/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
]




