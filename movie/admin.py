from django.contrib import admin
from .models import Movie, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")  # Show ID and Name in admin
    search_fields = ("name",)  # Allow searching by name

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "release_date")  # Show title and release date
    search_fields = ("title",)
    list_filter = ("categories",)  # Filter by categories

# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ("id", "movie")  # Show ID and Name in admin
#     search_fields = ("movie",) 