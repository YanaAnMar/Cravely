from django.shortcuts import render, get_object_or_404
from .models import Recipe, RecipeIngredient
from django.contrib.auth.models import User

# Create your views here.

def homepage(request):
    return render(request, '../templates/homepage.html')

def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {
        'profile_user': user_profile
    })

def recipepage(request, recipe_id):
    single_recipe = get_object_or_404(Recipe, id=recipe_id)
    steps_list = single_recipe.steps.split('|')
    ingredients_list = RecipeIngredient.objects.filter(recipe=single_recipe)
    return render(request, 'recipepage.html', {
        'recipe': single_recipe,
        'steps_list': steps_list,
        'ingredients_list': ingredients_list
    })

def saved_recipes(request):
    return render(request, '../templates/saved_recipes.html')

def add_recipe(request):
    return render(request, '../templates/add_recipe.html')