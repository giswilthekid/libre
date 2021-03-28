from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='libre-home'),
    path('register/', views.register, name='libre-register'),
    path('login/', views.login, name='libre-login'),
]