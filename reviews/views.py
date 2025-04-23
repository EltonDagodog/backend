from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Review, Comment, Reaction
from .serializers import ReviewSerializer, CommentSerializer, ReactionSerializer
from movie.models import Movie
from movie.serializer import MovieSerializer


class ReviewCreateOrUpdateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        movie_id = request.data.get("movie")
        rating = request.data.get("rating")

        if not movie_id or not rating:
            return Response({"error": "Movie ID and rating are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a review already exists for this user & movie
        review, created = Review.objects.update_or_create(
            user=request.user,
            movie_id=movie_id,
            defaults={"rating": rating}
        )

        if created:
            return Response({"message": "Review created successfully.", "review": ReviewSerializer(review).data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Review updated successfully.", "review": ReviewSerializer(review).data}, status=status.HTTP_200_OK)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return Response({'error': 'You can only delete your own review!'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

class RatingDetailView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movie_id = self.kwargs.get("movie_id")
        if movie_id is None:
            return Review.objects.none()  # Return empty queryset if movie_id is missing
        return Review.objects.filter(user=self.request.user, movie_id=movie_id)


#  Comment Views
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # ✅ Ensure user is authenticated

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return Response({'error': 'You can only delete your own comment!'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
    
class MovieCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Comment.objects.filter(movie_id=movie_id).order_by('-created_at')  # Show newest comments first



#  Reaction Views
class ToggleHeartView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        user = request.user
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        
        reaction, created = Reaction.objects.get_or_create(user=user, movie=movie, defaults={"reaction": "love"})

        if not created:  
            reaction.delete()
            hearted = False
        else:
            hearted = True  

        total_hearts = movie.reactions.count()  

        return Response({"hearted": hearted, "total_hearts": total_hearts}, status=status.HTTP_200_OK)


class MovieReactionsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id):
        user = request.user
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user hearted this movie
        hearted = Reaction.objects.filter(movie=movie, user=user, reaction="love").exists()

        # Count total hearts
        total_hearts = movie.reactions.count()

        return Response({
            "hearted": hearted,
            "total_hearts": total_hearts
        }, status=status.HTTP_200_OK)
    
class FavoriteMoviesListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        liked_movies = Reaction.objects.filter(user=user, reaction='love').select_related('movie')
        return [reaction.movie for reaction in liked_movies]
