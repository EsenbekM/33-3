from django.urls import path

from users import views


urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    path('profile/', views.profile),
    # path('verify/', views.verify),
]
