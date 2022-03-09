from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('usearch', views.usearch, name='userch'),
    path('username',views.showusername, name='username'),
    path('everyusersearch/<str:pk>/',views.everyusersearch,name='everyusersearch'),

    path('tuto/<str:pk>/', views.tuto,name='tuto'),
    
    path('login/',views.loginUser, name='login'),
    path('register/',views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),
    path('timerange/',views.timerange, name='timerange'),
]