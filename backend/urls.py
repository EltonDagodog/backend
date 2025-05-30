from django.contrib import admin
from django.urls import path, include  # Import `include`
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movie/', include('movie.urls')), 
    path('users/', include('users.urls')), 
    path('api/', include('reviews.urls')), 
    path('silk/', include('silk.urls', namespace='silk'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
