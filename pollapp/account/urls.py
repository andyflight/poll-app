from django.urls import path
from account import views

urlpatterns = [
path('login/', views.log_in, name='login'),
path('register/', views.register, name='register'),
path('logout', views.log_out, name='logout')
]
