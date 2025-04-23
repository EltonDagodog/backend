from rest_framework import serializers
from .models import Review, Comment, Reaction
from movie.models import Movie

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'rating', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        if "movie" not in data:
            raise serializers.ValidationError({"movie": "Movie ID is required."})
        if data["rating"] < 1 or data["rating"] > 5:
            raise serializers.ValidationError({"rating": "Rating must be between 1 and 5."})
        return data



class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'movie', 'user', 'text', 'created_at']
        read_only_fields = ['user', 'created_at']


class ReactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Reaction
        fields = ['id', 'movie', 'user', 'reaction', 'created_at']
        read_only_fields = ['user', 'created_at']
