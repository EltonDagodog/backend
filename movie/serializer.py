from rest_framework import serializers
from .models import Movie, Category
from reviews.models import  Review, Comment, Reaction
from django.db.models import Sum
from django.db.models import Avg

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class MovieSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True) 
    total_ratings = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    total_reactions = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "video", "image", "categories",
                  'total_ratings', 'total_comments', 'total_reactions']


    def get_total_ratings(self, obj):
        avg_rating = obj.reviews.aggregate(avg=Avg("rating"))["avg"]
        return round(avg_rating, 1) if avg_rating is not None else 0.0
            
    
    def get_total_comments(self, obj):
        return obj.comments.count()  

    def get_total_reactions(self, obj):
        return obj.reactions.count() 


# class MovieSerializer(serializers.ModelSerializer):
#     categories = CategorySerializer(many=True) 
    # average_rating = serializers.SerializerMethodField() 
    # total_reviews = serializers.SerializerMethodField()
    # total_comments = serializers.SerializerMethodField()  # Add total comments
    # comments = serializers.SerializerMethodField()

    # class Meta:
    #     model = Movie
    #     fields = ["id", "title", "description", "release_date", "video", "image", "categories",
    #               'total_reviews', 'total_comments', 'total_reactions']

    # def get_average_rating(self, obj):
    #     reviews = obj.reviews.all()
    #     return sum(review.rating for review in reviews) / len(reviews) if reviews else 0  

    # def get_total_reviews(self, obj):
    #     return obj.reviews.count() 

    # def get_total_comments(self, obj):
    #     return obj.reviews.exclude(comment="").count()  
    
    # def get_comments(self, obj):
    #     return [{"user": review.user.username, "comment": review.comment, "created_at": review.created_at} for review in obj.reviews.all()]


# class ReviewSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()  # Show username instead of ID

#     class Meta:
#         model = Review
#         fields = ['id', 'user', 'movie', 'rating', 'comment', 'created_at']
