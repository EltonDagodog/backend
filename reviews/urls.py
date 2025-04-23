from django.urls import path
from .views import (
    ReviewCreateOrUpdateView, ReviewDetailView,
    CommentListCreateView, CommentDetailView,
    ToggleHeartView, MovieReactionsView, MovieCommentsView, CommentCreateView,RatingDetailView,FavoriteMoviesListView
)

urlpatterns = [
    # Reviews
    path('reviews/', ReviewCreateOrUpdateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('ratings/<int:movie_id>/', RatingDetailView.as_view(), name='user-review-detail'),


    # Comments
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('movies/<int:movie_id>/comments/', MovieCommentsView.as_view(), name='movie-comments'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),

    # Reactions
   
    path("movies/<int:movie_id>/reactions/", MovieReactionsView.as_view(), name="get-movie-reactions"),
    path("movies/<int:movie_id>/react/", ToggleHeartView.as_view(), name="toggle-heart"),
    path('movies/favorites/', FavoriteMoviesListView.as_view(), name='favorite-movies'),
]
