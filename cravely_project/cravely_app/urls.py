from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name= 'homepage'),
    path('profile/update-blacklist/', views.update_blacklist, name='update_blacklist'),
    path('profile/<str:username>/', views.profile, name = 'profile'),
    path('recipe/<int:recipe_id>/', views.recipepage, name = 'recipepage'),
    #path('recipepage/', views.recipepage, name = 'recipepage'),

    path('saved/', views.saved_recipes, name='saved_recipes'),
    path('recipe/<int:recipe_id>/save/', views.toggle_save, name='toggle_save'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('lookup/', views.lookup, name='lookup'),
    #path('ime/', views.ime, name = 'ime'),
]
