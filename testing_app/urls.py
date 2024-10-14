from django.urls import path
from testing_app import views

urlpatterns = [
    path('post/register/', views.UserRegister, name='registration'),
    path('post/login/', views.UserLogin, name='login'),
]
