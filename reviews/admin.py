from django.contrib import admin
from .models import Comment, Review, Reaction

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie', 'rating', 'created_at')  
    
    readonly_fields = ('id',) 
    

admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment)
admin.site.register(Reaction)