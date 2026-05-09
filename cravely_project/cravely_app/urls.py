from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name= 'homepage'),
    path('profile/', views.profile, name = 'profile'),
    #path('ime/', views.ime, name = 'ime'),
]