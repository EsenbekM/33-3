from django.contrib import admin
from django.urls import path
from news import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.hello_world),

    path('api/v1/news/', views.get_news),
    path('api/v1/news/<int:news_id>/', views.get_news_by_id),
    path('api/v1/comments/', views.comments_list),
]
