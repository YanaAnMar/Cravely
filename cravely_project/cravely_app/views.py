from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Create your views here.

def homepage(request):
    return render(request, '../templates/homepage.html')

def profile(request):
    return render(request, '../templates/profile.html')

def recipepage(request, recipe_id):
    single_recipe = get_object_or_404(Recipe, id=recipe_id)
    steps_list = single_recipe.steps.split('|')
    return render(request, 'recipepage.html', {
        'recipe': single_recipe,
        'steps_list': steps_list
    })

def saved_recipes(request):
    return render(request, '../templates/saved_recipes.html')

def add_recipe(request):
    return render(request, '../templates/add_recipe.html')