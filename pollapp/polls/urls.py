from django.urls import path
from polls import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('add-poll/', views.add_poll, name='add poll'),
    path('polls/<int:poll_id>/vote', views.poll, name='detail'),
    path('polls/<int:poll_id>/results/', views.poll_results, name='results'),
    path('my-polls/', views.my_polls, name='my polls'),
    path('my-polls/<int:poll_id>/delete/', views.delete_poll, name='delete'),
    path('my-polls/<int:poll_id>/stop/', views.stop_poll, name='stop')
]
