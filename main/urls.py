from django.contrib import admin
from django.urls import include, path
from main.drf_yasg import urlpatterns as yasg_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('news.urls')),
    path('api/v1/', include('users.urls')),
] + yasg_patterns
