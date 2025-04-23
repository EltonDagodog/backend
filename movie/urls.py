from django.urls import path
from .views import MovieListView, MovieDetailView

urlpatterns = [
    # path("api/movies/<int:movie_id>/add-comment/", add_comment, name="add_comment"),
    # path('movies/<int:movie_id>/reviews/', ReviewListCreateView.as_view(), name='movie-reviews'),
    path('api/movies/', MovieListView.as_view(), name='movie-list'),  # Get all movies
    path('api/movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),  # Get single movie by ID
  
]

