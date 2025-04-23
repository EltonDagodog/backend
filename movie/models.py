from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    video = models.FileField(upload_to='movies/videos/')  
    image = models.ImageField(upload_to='movies/images/', blank=True, null=True)  
    categories = models.ManyToManyField(Category, related_name="movies")  # Many-to-Many relationship

    # def average_rating(self):
    #     reviews = self.reviews.all()
    #     if reviews:
    #         return sum(review.rating for review in reviews) / len(reviews)
    #     return 0  

    def __str__(self):
        return self.title

# class Review(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
#     rating = models.IntegerField(default=1)  # 1 to 5 stars
#     comment = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'movie')  # Ensures a user can only review a movie once

#     def __str__(self):
#         return f"{self.user.username} rated {self.movie.title} {self.rating}/5"
