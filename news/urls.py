from django.urls import path
from news import views


urlpatterns = [
    path('test/', views.hello_world),
    path('news/', views.get_news), # GET -> list, POST -> create
    path('news/<int:news_id>/', views.get_news_by_id), # GET -> retrieve, PUT -> update, DELETE -> delete
    path('comments/', views.comments_list),
]
