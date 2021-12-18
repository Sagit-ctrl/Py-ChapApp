from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register/checkregister', views.checkregister, name='checkregister'),
    path('create_room/', views.create_room, name='create_room'),
    path('home/', views.home, name='home'),
    path('<str:room>/', views.room, name='room'),
    path('home/checkview', views.checkview, name='checkview'),
    path('checklogin', views.checklogin, name='checklogin'),
    path('create_room/checkroom', views.checkroom, name='checkroom'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('getRoom/<str:username>/', views.getRoom, name='getRoom'),
]