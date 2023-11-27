from django.contrib import admin
from django.urls import include, path
from news import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('news.urls')),
    path('api/v1/', include('users.urls')),
]
