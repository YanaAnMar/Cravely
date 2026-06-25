from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homepage, name= 'homepage'),
    path('profile/update-blacklist/', views.update_blacklist, name='update_blacklist'),
    path('profile/<str:username>/', views.profile, name = 'profile'),
    path('recipe/<int:recipe_id>/', views.recipepage, name = 'recipepage'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('saved/', views.saved_recipes, name='saved_recipes'),
    path('recipe/<int:recipe_id>/save/', views.toggle_save, name='toggle_save'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('lookup/', views.lookup, name='lookup'),
    #path('ime/', views.ime, name = 'ime'),
]
