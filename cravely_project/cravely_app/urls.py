from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name= 'homepage'),
    path('profile/', views.profile, name = 'profile'),
    path('recipepage/', views.recipepage, name = 'recipepage'),
    path('saved/', views.saved_recipes, name='saved_recipes'),
    #path('ime/', views.ime, name = 'ime'),
]